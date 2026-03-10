import base64
from datetime import date, timedelta
from io import BytesIO

import qrcode
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


# ==========================================
# 0. MODELOS DE CONFIGURACIÓN (Diccionarios)
# ==========================================
class InventoryCategory(models.Model):
    _name = "inventory.category"
    _description = "Categoría de Activo"
    _rec_name = "nombre"

    active = fields.Boolean(string="Activo", default=True)
    nombre = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True, help="Ej: APP, HW, NET...")
    descripcion = fields.Text(string="Descripción")

    def unlink(self):
        for record in self:
            # Verificar si hay activos vinculados a esta categoría
            assets = self.env["inventory.asset"].search([("categoria_id", "=", record.id)], limit=1)
            if assets:
                raise UserError(f"No puedes eliminar la categoría '{record.nombre}' porque tiene activos asociados.")
        return super(InventoryCategory, self).unlink()


class InventorySubcategory(models.Model):
    _name = "inventory.subcategory"
    _description = "Subcategoría de Activo"
    _rec_name = "nombre"

    active = fields.Boolean(string="Activo", default=True)
    nombre = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True, help="Ej: SRV, LAP, NVG...")
    descripcion = fields.Text(string="Descripción")
    categoria_id = fields.Many2one("inventory.category", string="Categoría", required=True, ondelete="cascade")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("categoria_id"):
                raise ValidationError("La subcategoría debe estar vinculada a una categoría.")
        return super(InventorySubcategory, self).create(vals_list)

    def write(self, vals):
        if "categoria_id" in vals and not vals.get("categoria_id"):
            raise ValidationError("La subcategoría debe estar vinculada a una categoría.")
        return super(InventorySubcategory, self).write(vals)

    @api.constrains("categoria_id")
    def _check_categoria_id(self):
        for record in self:
            if not record.categoria_id:
                raise ValidationError("La subcategoría debe estar vinculada a una categoría.")


class InventoryLocation(models.Model):
    _name = "inventory.location"
    _description = "Localización de Activo"
    _rec_name = "nombre"

    active = fields.Boolean(string="Activo", default=True)
    nombre = fields.Char(string="Nombre", required=True)
    codigo = fields.Char(string="Código", required=True, help="Ej: BOA, ILAB, AWS...")
    descripcion = fields.Text(string="Descripción")

    def unlink(self):
        for record in self:
            # Verificar si hay activos vinculados a esta ubicación
            assets = self.env["inventory.asset"].search([("ubicacion_id", "=", record.id)], limit=1)
            if assets:
                raise UserError(f"No puedes eliminar la localización '{record.nombre}' porque tiene activos asociados.")
        return super(InventoryLocation, self).unlink()


# ==========================================
# SUB-MODELOS PARA EL PLAN (Tareas y Alertas)
# ==========================================
class PlansTask(models.Model):
    _name = "plans.task"
    _description = "Tareas de Mantenimiento"

    name = fields.Char(string="Descripción de la tarea", required=True)
    plan_id = fields.Many2one("plans.asset", string="Plan", ondelete="cascade")


class PlansAlert(models.Model):
    _name = "plans.alert"
    _description = "Reglas de Alertas"

    plan_id = fields.Many2one("plans.asset", string="Plan", ondelete="cascade")
    valor = fields.Integer(string="Cantidad de tiempo", required=True, default=1)
    unidad = fields.Selection(
        [("days", "Días"), ("weeks", "Semanas")],
        string="Unidad",
        required=True,
        default="weeks",
    )

    name = fields.Char(compute="_compute_name")

    @api.depends("valor", "unidad")
    def _compute_name(self):
        for rec in self:
            u = "Días" if rec.unidad == "days" else "Semanas"
            rec.name = f"{rec.valor} {u} antes"


# ==========================================
# EL PLAN DE MANTENIMIENTO
# ==========================================
class PlansAsset(models.Model):
    _name = "plans.asset"
    _description = "Planes de Mantenimiento"
    _rec_name = "nombre"

    identificador = fields.Char(string="Identificador", default="Nuevo", readonly=True, copy=False)
    active = fields.Boolean(string="Activo", default=True, help="Desmarca para dar de baja el plan")
    nombre = fields.Char(string="Nombre del Plan", required=True)

    # Vinculado a la tabla relacional
    categoria_id = fields.Many2one("inventory.category", string="Categoría asociada", required=True)
    subcategoria_id = fields.Many2one(
        "inventory.subcategory",
        string="Tipología de activo asociada",
        required=True,
        domain="[('categoria_id', '=', categoria_id)]",
    )

    periodicidad = fields.Selection(
        [
            ("7", "Semanal"),
            ("15", "Quincenal"),
            ("30", "Mensual"),
            ("90", "Trimestral"),
            ("180", "Semestral"),
            ("365", "Anual"),
        ],
        string="Periodicidad",
        required=True,
        default="30",
    )

    tarea_ids = fields.One2many("plans.task", "plan_id", string="Tareas a realizar")
    alerta_ids = fields.One2many("plans.alert", "plan_id", string="Alertas Previas")
    alerta_recurrente = fields.Boolean(string="Alertar cada semana si está vencido", default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("identificador", "Nuevo") == "Nuevo":
                vals["identificador"] = self.env["ir.sequence"].next_by_code("plans.asset.sequence") or "Nuevo"
        return super(PlansAsset, self).create(vals_list)


# ==========================================
# NUEVOS MODELOS DE SEGUIMIENTO (CHECKLIST E HISTORIAL)
# ==========================================
class InventoryAssetMaintenance(models.Model):
    _name = "inventory.asset.maintenance"
    _description = "Instancia de Mantenimiento de Activo"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "fecha_inicio desc"

    asset_id = fields.Many2one("inventory.asset", string="Activo", required=True, ondelete="cascade")
    plan_id = fields.Many2one("plans.asset", string="Plan Original")

    fecha_inicio = fields.Date(string="Fecha de Inicio", default=fields.Date.today(), tracking=True)
    fecha_fin = fields.Date(string="Fecha de Finalización", readonly=True, tracking=True)

    notas_generales = fields.Text(string="Notas Generales", tracking=True)

    state = fields.Selection(
        [("in_progress", "En Proceso"), ("done", "Realizado")],
        string="Estado",
        default="in_progress",
        tracking=True,
    )

    checklist_line_ids = fields.One2many("inventory.asset.maintenance.line", "maintenance_id", string="Checklist")

    display_name = fields.Char(compute="_compute_display_name")

    @api.depends("asset_id", "plan_id", "fecha_inicio")
    def _compute_display_name(self):
        for rec in self:
            plan_name = rec.plan_id.nombre if rec.plan_id else "Mantenimiento"
            rec.display_name = f"{plan_name} - {rec.asset_id.nombre} ({rec.fecha_inicio})"

    def write(self, vals):
        if "notas_generales" in vals:
            for record in self:
                old_note = record.notas_generales or "vacio"
                new_note = vals["notas_generales"] or "vacio"
                msg = f"Notas Generales cambiadas de '{old_note}' a '{new_note}'"

                # Post to THIS record chatter
                record.message_post(body=msg)

                # Post to asset record
                if record.asset_id:
                    asset_msg = f"Mantenimiento ({record.display_name}): {msg}"
                    record.asset_id.message_post(body=asset_msg)
        return super(InventoryAssetMaintenance, self).write(vals)

    def unlink(self):
        for record in self:
            if record.state == "done" and not self.env.user.has_group("base.group_erp_manager"):
                raise UserError("No puedes eliminar un registro de mantenimiento que ya ha sido finalizado. Contacta con tu administrador.")
        return super(InventoryAssetMaintenance, self).unlink()


class InventoryAssetMaintenanceLine(models.Model):
    _name = "inventory.asset.maintenance.line"
    _description = "Línea de Checklist de Mantenimiento"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    maintenance_id = fields.Many2one("inventory.asset.maintenance", string="Mantenimiento", ondelete="cascade")
    name = fields.Char(string="Tarea", required=True, tracking=True)
    is_done = fields.Boolean(string="Hecho", default=False, tracking=True)
    image = fields.Binary(string="Imagen / Evidencia")
    notes = fields.Char(string="Notas adicionales", tracking=True)

    def write(self, vals):
        # Post to parent maintenance AND asset chatter if notes or image changed
        for record in self:
            changes = []
            if "notes" in vals:
                old_note = record.notes or "vacio"
                new_note = vals["notes"] or "vacio"
                changes.append(f"Notas de '{record.name}' cambiadas de '{old_note}' a '{new_note}'")
            if "image" in vals:
                changes.append(f"Se ha actualizado la imagen de la tarea '{record.name}'")

            if changes and record.maintenance_id:
                msg = " | ".join(changes)
                # Post to maintenance record chatter
                record.maintenance_id.message_post(body=msg)

                # Post to asset record
                if record.maintenance_id.asset_id:
                    asset_msg = f"Mantenimiento ({record.maintenance_id.display_name}): {msg}"
                    record.maintenance_id.asset_id.message_post(body=asset_msg)

        return super(InventoryAssetMaintenanceLine, self).write(vals)


# ==========================================
# EL ACTIVO (InventoryAsset)
# ==========================================
class InventoryAsset(models.Model):
    _name = "inventory.asset"
    _description = "Inventario de Activos"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "nombre"

    @api.constrains("identificador_final")
    def _check_identificador_final_unique(self):
        for record in self:
            if record.identificador_final:
                duplicate = self.search(
                    [
                        ("identificador_final", "=", record.identificador_final),
                        ("id", "!=", record.id),
                    ],
                    limit=1,
                )
                if duplicate:
                    raise ValidationError(f"El Identificador Estandarizado '{record.identificador_final}' ya está en uso por otro activo.")

    active = fields.Boolean(string="Activo", default=True, tracking=True)
    nombre = fields.Char(string="Nombre", required=True, tracking=True)
    descripcion = fields.Text(string="Descripción")
    detalles_adicionales = fields.Text(string="Detalles adicionales")

    tipo = fields.Char(string="Tipo")
    localizacion = fields.Char(string="Localización (Texto libre)")

    tipo_responsable = fields.Selection(
        [("empleado", "Empleado"), ("departamento", "Departamento")],
        string="Tipo de Responsable",
        default="empleado",
        tracking=True,
    )
    responsable_empleado_id = fields.Many2one("hr.employee", string="Responsable (Empleado)", tracking=True)
    responsable_departamento_id = fields.Many2one("hr.department", string="Responsable (Departamento)", tracking=True)

    tipo_propietario = fields.Selection(
        [("empleado", "Empleado"), ("departamento", "Departamento")],
        string="Tipo de Propietario",
        default="empleado",
        tracking=True,
    )
    propietario_empleado_id = fields.Many2one("hr.employee", string="Propietario (Empleado)", tracking=True)
    propietario_departamento_id = fields.Many2one("hr.department", string="Propietario (Departamento)", tracking=True)

    responsable_display = fields.Char(string="Responsable", compute="_compute_responsable_display")
    propietario_display = fields.Char(string="Propietario", compute="_compute_propietario_display")

    # Relación con el historial de asignaciones
    history_ids = fields.One2many("inventory.asset.history", "asset_id", string="Historial de Asignaciones")

    @api.depends("tipo_responsable", "responsable_empleado_id", "responsable_departamento_id")
    def _compute_responsable_display(self):
        for record in self:
            if record.tipo_responsable == "empleado" and record.responsable_empleado_id:
                record.responsable_display = record.responsable_empleado_id.name
            elif record.tipo_responsable == "departamento" and record.responsable_departamento_id:
                record.responsable_display = record.responsable_departamento_id.name
            else:
                record.responsable_display = "Sin asignar"

    @api.depends("tipo_propietario", "propietario_empleado_id", "propietario_departamento_id")
    def _compute_propietario_display(self):
        for record in self:
            if record.tipo_propietario == "empleado" and record.propietario_empleado_id:
                record.propietario_display = record.propietario_empleado_id.name
            elif record.tipo_propietario == "departamento" and record.propietario_departamento_id:
                record.propietario_display = record.propietario_departamento_id.name
            else:
                record.propietario_display = "Sin asignar"

    hardware = fields.Char(string="Hardware")
    os = fields.Char(string="Sistema Operativo")
    version = fields.Char(string="Versión S.O. / App")
    notas = fields.Text(string="Observaciones")

    ultimomantenimiento = fields.Date(string="Ultimo Mantenimiento", readonly=True)
    proximo_mantenimiento = fields.Date(string="Próximo Mantenimiento", tracking=True)

    # Filtro automático
    plan_id = fields.Many2one(
        "plans.asset",
        string="Plan de Mantenimiento",
        tracking=True,
        domain="[('subcategoria_id', '=', subcategoria_id)]",
    )

    # --- Seguimiento de Mantenimiento ---
    estado_mantenimiento_proceso = fields.Selection(
        [
            ("no_iniciado", "No Iniciado"),
            ("en_proceso", "En Proceso"),
            ("realizado", "Realizado"),
        ],
        string="Estado Proceso Mant.",
        default="no_iniciado",
        tracking=True,
    )

    mantenimiento_activo_id = fields.Many2one("inventory.asset.maintenance", string="Mantenimiento Actual", readonly=True)

    # Campo relacionado para mostrar y editar las líneas del mantenimiento activo desde el activo
    checklist_activo_ids = fields.One2many(
        "inventory.asset.maintenance.line",
        related="mantenimiento_activo_id.checklist_line_ids",
        readonly=False,
        string="Tareas del Mantenimiento en Proceso",
    )

    mantenimiento_history_ids = fields.One2many(
        "inventory.asset.maintenance",
        "asset_id",
        string="Historial de Mantenimientos",
        domain=[("state", "=", "done")],
    )

    # ==========================================
    # CAMPOS RELACIONALES (Sustituyen a las listas fijas)
    # ==========================================
    categoria_id = fields.Many2one("inventory.category", string="Categoría", tracking=True)
    subcategoria_id = fields.Many2one(
        "inventory.subcategory",
        string="Subcategoría",
        tracking=True,
        domain="[('categoria_id', '=', categoria_id)]",
    )
    ubicacion_id = fields.Many2one("inventory.location", string="Localización", tracking=True)

    @api.onchange("categoria_id")
    def _onchange_categoria_id(self):
        """Clear subcategory when category changes"""
        if self.categoria_id:
            self.subcategoria_id = False

    uuid_activo = fields.Char(string="Identificador Único (UUID)", default="Nuevo", readonly=True, copy=False)
    anio_inclusion = fields.Char(string="Año de inclusión", default=lambda self: str(fields.Date.today().year))
    identificador_final = fields.Char(string="ID Estandarizado", compute="_compute_identificador_final", store=True)

    @api.depends(
        "categoria_id",
        "subcategoria_id",
        "ubicacion_id",
        "uuid_activo",
        "anio_inclusion",
    )
    def _compute_identificador_final(self):
        for record in self:
            # Ahora cogemos el .codigo del registro que se haya seleccionado en la tabla
            cat = record.categoria_id.codigo if record.categoria_id else "XXX"
            sub = record.subcategoria_id.codigo if record.subcategoria_id else "XXX"
            ubi = record.ubicacion_id.codigo if record.ubicacion_id else "XXX"
            uid = record.uuid_activo or "0000"
            anio = record.anio_inclusion or "XXXX"
            record.identificador_final = f"{cat}.{sub}.{ubi}.{uid}.{anio}"

    # Campo QR: ahora de tipo Binary para almacenar la imagen real
    qr_code = fields.Binary(string="Código QR", compute="_compute_qr_code")

    @api.depends("identificador_final")
    def _compute_qr_code(self):
        """
        Genera una imagen PNG del código QR que contiene la URL de la ficha del activo.
        """
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for record in self:
            if record.id:
                # URL de la ficha del producto en Odoo
                url = f"{base_url}/web#id={record.id}&model=inventory.asset&view_type=form"

                # Generación del código QR
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)

                img = qr.make_image(fill_color="black", back_color="white")

                # Guardar la imagen en un buffer para convertirla a base64
                stream = BytesIO()
                img.save(stream, format="PNG")
                record.qr_code = base64.b64encode(stream.getvalue())
            else:
                record.qr_code = False

    estado_mantenimiento = fields.Selection(
        [("normal", "Normal"), ("proximo", "Próximo"), ("vencido", "Vencido")],
        compute="_compute_estado_mantenimiento",
        string="Estado",
    )

    @api.depends("proximo_mantenimiento")
    def _compute_estado_mantenimiento(self):
        hoy = fields.Date.today()
        for activo in self:
            if not activo.proximo_mantenimiento:
                activo.estado_mantenimiento = "normal"
            elif activo.proximo_mantenimiento < hoy:
                activo.estado_mantenimiento = "vencido"
            elif activo.proximo_mantenimiento <= (hoy + timedelta(days=7)):
                activo.estado_mantenimiento = "proximo"
            else:
                activo.estado_mantenimiento = "normal"

    @api.model
    def check_maintenance_dates(self):
        hoy = date.today()
        activos = self.search([("proximo_mantenimiento", "!=", False)])

        for asset in activos:
            plan = asset.plan_id
            if not plan:
                continue

            user_to_notify = False
            if asset.tipo_responsable == "empleado" and asset.responsable_empleado_id.user_id:
                user_to_notify = asset.responsable_empleado_id.user_id.id
            elif asset.tipo_responsable == "departamento" and asset.responsable_departamento_id.manager_id.user_id:
                user_to_notify = asset.responsable_departamento_id.manager_id.user_id.id

            if not user_to_notify:
                continue

            dias_restantes = (asset.proximo_mantenimiento - hoy).days
            crear_alerta = False
            msg = ""

            if dias_restantes == 0:
                crear_alerta = True
                msg = "¡Mantenimiento HOY!"
            elif dias_restantes > 0:
                for alerta in plan.alerta_ids:
                    dias_para_alerta = alerta.valor * (7 if alerta.unidad == "weeks" else 1)
                    if dias_restantes == dias_para_alerta:
                        crear_alerta = True
                        msg = f"Recordatorio: Mantenimiento en {dias_restantes} días"
                        break
            elif dias_restantes < 0 and plan.alerta_recurrente:
                dias_atraso = abs(dias_restantes)
                if dias_atraso % 7 == 0:
                    crear_alerta = True
                    msg = f"¡URGENTE! Mantenimiento atrasado por {dias_atraso} días"

            if crear_alerta:
                self.env["mail.activity"].create(
                    {
                        "res_id": asset.id,
                        "res_model_id": self.env.ref("Inventario.model_inventory_asset").id,
                        "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                        "summary": msg,
                        "note": f"Revisa el plan '{plan.nombre}' para: {asset.nombre}. ID: {asset.identificador_final}",
                        "user_id": user_to_notify,
                        "date_deadline": asset.proximo_mantenimiento,
                    }
                )

    def action_maintenance_done(self):
        for asset in self:
            dias = int(asset.plan_id.periodicidad) if asset.plan_id and asset.plan_id.periodicidad else 30
            hoy = fields.Date.today()
            asset.ultimomantenimiento = hoy
            asset.proximo_mantenimiento = hoy + timedelta(days=dias)
            asset.message_post(body=f"✅ Tarea completada. Próxima fecha: {asset.proximo_mantenimiento}")
            activity_ids = asset.activity_ids.filtered(lambda a: a.activity_type_id.name == "To Do")
            if activity_ids:
                activity_ids.action_done()

    # --- Nuevas Acciones de Mantenimiento Integrado ---
    def action_start_maintenance(self):
        """
        Inicia un proceso de mantenimiento:
        1. Cambia estado a 'en_proceso'
        2. Crea una instancia de mantenimiento con checklist basado en el plan
        """
        for asset in self:
            if not asset.plan_id:
                raise UserError("Selecciona primero un plan de mantenimiento para este activo.")

            if asset.mantenimiento_activo_id:
                raise UserError("⚠️ Ya hay un mantenimiento en proceso para este activo.")

            # Crear la instancia
            maintenance = self.env["inventory.asset.maintenance"].create(
                {
                    "asset_id": asset.id,
                    "plan_id": asset.plan_id.id,
                    "fecha_inicio": fields.Date.today(),
                    "state": "in_progress",
                }
            )

            # Copiar tareas del plan al checklist de la instancia
            lines = []
            for task in asset.plan_id.tarea_ids:
                lines.append((0, 0, {"name": task.name, "is_done": False}))

            maintenance.write({"checklist_line_ids": lines})

            # Actualizar el activo
            asset.write(
                {
                    "estado_mantenimiento_proceso": "en_proceso",
                    "mantenimiento_activo_id": maintenance.id,
                }
            )

            asset.message_post(body=f"🛠️ Mantenimiento iniciado usando el plan: {asset.plan_id.nombre}")

    def action_finish_maintenance(self):
        """
        Finaliza el proceso de mantenimiento:
        1. Verifica que haya un mantenimiento activo
        2. Cambia estado a 'realizado'
        3. Actualiza fechas de mantenimiento del activo
        4. Cierra la instancia de mantenimiento
        """
        for asset in self:
            if not asset.mantenimiento_activo_id:
                raise UserError("⚠️ No hay ningún mantenimiento en proceso para finalizar.")

            # Validar que todo el checklist esté hecho (opcional, pero recomendado)
            if not all(asset.mantenimiento_activo_id.checklist_line_ids.mapped("is_done")):
                asset.message_post(body="ℹ️ Finalizando mantenimiento con tareas pendientes.")

            # Cerrar la instancia
            instance = asset.mantenimiento_activo_id
            instance.write({"state": "done", "fecha_fin": fields.Date.today()})

            # Actualizar fechas del activo (reutilizando lógica de action_maintenance_done)
            asset.action_maintenance_done()

            # Limpiar activo y marcar como realizado
            asset.write(
                {
                    "estado_mantenimiento_proceso": "realizado",
                    "mantenimiento_activo_id": False,
                }
            )

            asset.message_post(body="✅ Proceso de mantenimiento finalizado y registrado en el historial.")

    def action_archive(self):
        for record in self:
            if record.tipo_propietario == "empleado" and record.propietario_empleado_id:
                raise UserError(f"⛔ No puedes dar de baja '{record.nombre}' porque todavía pertenece a {record.propietario_empleado_id.name}.")
            elif record.tipo_propietario == "departamento" and record.propietario_departamento_id:
                raise UserError(
                    f"⛔ No puedes dar de baja '{record.nombre}' porque pertenece al departamento de {record.propietario_departamento_id.name}."
                )
        return super(InventoryAsset, self).action_archive()

    def unlink(self):
        for record in self:
            if record.tipo_propietario == "empleado" and record.propietario_empleado_id:
                raise UserError(f"⛔ No puedes eliminar '{record.nombre}' porque tiene un propietario asignado.")
            elif record.tipo_propietario == "departamento" and record.propietario_departamento_id:
                raise UserError(f"⛔ No puedes eliminar '{record.nombre}' porque tiene un departamento asignado.")
        return super(InventoryAsset, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("uuid_activo", "Nuevo") == "Nuevo":
                vals["uuid_activo"] = self.env["ir.sequence"].next_by_code("inventory.asset.sequence") or "Nuevo"

            # Manual unique check before hitting the database
            # We must compute the identifier first if it's based on values in vals
            # For simplicity, we can just rely on the fact that if we are providing
            # a uuid_activo and anio_inclusion that already exists, it will fail.
            if "identificador_final" in vals:
                duplicate = self.search([("identificador_final", "=", vals["identificador_final"])], limit=1)
                if duplicate:
                    raise ValidationError(f"El Identificador Estandarizado '{vals['identificador_final']}' ya está en uso.")

        records = super(InventoryAsset, self).create(vals_list)
        for record in records:
            record._compute_identificador_final()

            # Registro inicial en el historial si hay empleados asignados al crear
            if record.responsable_empleado_id:
                self.env["inventory.asset.history"].create(
                    {
                        "asset_id": record.id,
                        "new_employee_id": record.responsable_empleado_id.id,
                        "role": "responsible",
                        "date": fields.Date.today(),
                    }
                )
            if record.propietario_empleado_id:
                self.env["inventory.asset.history"].create(
                    {
                        "asset_id": record.id,
                        "new_employee_id": record.propietario_empleado_id.id,
                        "role": "owner",
                        "date": fields.Date.today(),
                    }
                )

        return records

    def write(self, vals):
        """
        Sobrescribimos write para capturar cambios en el responsable y propietario
        y registrarlos en el historial de trazabilidad.
        """
        for record in self:
            # Detectar cambio de responsable
            if "responsable_empleado_id" in vals:
                old_id = record.responsable_empleado_id.id
                new_id = vals.get("responsable_empleado_id")
                if old_id != new_id:
                    self.env["inventory.asset.history"].create(
                        {
                            "asset_id": record.id,
                            "old_employee_id": old_id,
                            "new_employee_id": new_id,
                            "role": "responsible",
                            "date": fields.Date.today(),
                        }
                    )

            # Detectar cambio de propietario
            if "propietario_empleado_id" in vals:
                old_id = record.propietario_empleado_id.id
                new_id = vals.get("propietario_empleado_id")
                if old_id != new_id:
                    self.env["inventory.asset.history"].create(
                        {
                            "asset_id": record.id,
                            "old_employee_id": old_id,
                            "new_employee_id": new_id,
                            "role": "owner",
                            "date": fields.Date.today(),
                        }
                    )

        return super(InventoryAsset, self).write(vals)


# ==========================================
# HISTORIAL DE ASIGNACIONES (Traceability)
# ==========================================
class InventoryAssetHistory(models.Model):
    _name = "inventory.asset.history"
    _description = "Historial de Asignaciones de Activos"
    _order = "date desc, id desc"

    asset_id = fields.Many2one("inventory.asset", string="Activo", required=True, ondelete="cascade")
    identificador_final = fields.Char(related="asset_id.identificador_final", string="ID Estandarizado", store=True)
    old_employee_id = fields.Many2one("hr.employee", string="Anterior Empleado")
    new_employee_id = fields.Many2one("hr.employee", string="Nuevo Empleado")
    role = fields.Selection(
        [("owner", "Propietario"), ("responsible", "Responsable")],
        string="Rol",
        required=True,
    )
    date = fields.Date(string="Fecha de Cambio", default=fields.Date.today(), required=True)


# ==========================================
# EXTENSIÓN DE EMPLEADO (hr.employee)
# ==========================================
class HrEmployee(models.Model):
    """
    Extendemos el modelo de empleados para permitir la trazabilidad inversa
    desde el propio empleado hacia sus activos asignados.
    """

    _inherit = "hr.employee"

    # Activos donde el empleado es el responsable actual
    current_responsible_asset_ids = fields.One2many(
        "inventory.asset",
        "responsable_empleado_id",
        string="Activos bajo su Responsabilidad (Actual)",
    )

    # Activos donde el empleado es el propietario actual
    current_owner_asset_ids = fields.One2many(
        "inventory.asset",
        "propietario_empleado_id",
        string="Activos en Propiedad (Actual)",
    )

    # Historial completo de activos que han pasado por este empleado
    asset_history_ids = fields.One2many(
        "inventory.asset.history",
        "new_employee_id",
        string="Historial de Activos Asignados",
    )

    # Campo computado para ver la lista de activos únicos que ha tenido históricamente
    historical_asset_ids = fields.Many2many(
        "inventory.asset",
        string="Activos Vinculados Históricamente",
        compute="_compute_historical_assets",
    )

    asset_count = fields.Integer(string="Cantidad de Activos", compute="_compute_asset_count")

    @api.depends("current_responsible_asset_ids", "current_owner_asset_ids")
    def _compute_asset_count(self):
        for employee in self:
            # Contamos activos únicos donde es responsable o propietario
            assets = employee.current_responsible_asset_ids | employee.current_owner_asset_ids
            employee.asset_count = len(assets)

    def action_view_employee_assets(self):
        """
        Acción para el Smart Button: redirige a la vista de activos del empleado.
        Usamos la acción personalizada que ya existe pero filtrando por el empleado.
        """
        self.ensure_one()
        action = self.env.ref("Inventario.action_inventory_employee").read()[0]
        # Forzamos que abra este empleado específico en modo formulario
        action["res_id"] = self.id
        action["view_mode"] = "form"
        action["views"] = [(self.env.ref("Inventario.view_employee_form_inventory_simple").id, "form")]
        return action

    @api.depends("asset_history_ids")
    def _compute_historical_assets(self):
        """Calcula los activos únicos que han estado vinculados al empleado"""
        for employee in self:
            assets = employee.asset_history_ids.mapped("asset_id")
            employee.historical_asset_ids = assets

    @api.model
    def _get_private_fields(self):
        """
        Agregamos nuestros campos personalizados a la lista de campos privados
        para evitar que Odoo lance un AccessError al intentar leerlos desde
        perfiles públicos si no se tiene el permiso adecuado.
        """
        res = super(HrEmployee, self)._get_private_fields()
        res.extend(
            [
                "current_responsible_asset_ids",
                "current_owner_asset_ids",
                "asset_history_ids",
                "historical_asset_ids",
            ]
        )
        return res
