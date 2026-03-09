from odoo import http
from odoo.http import request


class InventoryController(http.Controller):
    @http.route("/inventory/asset/print/<int:asset_id>", auth="user", type="http", website=True)
    def print_asset_label(self, asset_id, **kw):
        """
        Renders a preview page for the asset label and triggers the browser print dialog.
        """
        asset = request.env["inventory.asset"].browse(asset_id)
        if not asset.exists():
            return request.not_found()

        # We pass the asset data to a simple template that triggers print() on load
        return request.render(
            "Inventario.asset_label_preview_template",
            {
                "asset": asset,
            },
        )
