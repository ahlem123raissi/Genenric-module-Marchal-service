{
    "name": "Product Scrap",
    'version': "18.0",
    'category': "Sales/Sales",
       "summary": "Effortlessly relocate stock to the scrap location using a user-friendly interface.Manage scrap products efficiently from the product variants form view, with detailed scrap order and location tracking. scrap product management Odoo, track scrap products Odoo, Odoo inventory management, scrap location tracking, product waste management, Odoo scrap orders, scrap quantity tracking, inventory scrap management, Odoo smart button scrap, manage scrap orders Odoo, real-time inventory updates Odoo, scrap order reporting, Odoo product variants scrap, reduce inventory losses Odoo, scrap product functionality, Odoo stock level updates, manage product waste Odoo, Odoo inventory updates, scrap orders view Odoo, scrap management app Odoo, Odoo waste management",
    'description': """
    Scrap Product Management

    The Scrap Product app for Odoo provides businesses with a seamless way to manage product scrap directly from the Product Variants form view. With the addition of a smart button for "On Hand" quantity, users can scrap products and track them easily, including specifying scrap locations and quantities. This app enhances inventory management by integrating scrap orders into the Odoo system, helping businesses reduce inventory losses and keep accurate stock records.

    Key Features:
    - Scrap Management from Product Variants: Users can access a smart button for "On Hand" quantities in the product variants form view, which also includes the option to scrap products.
    - Scrap Location Tracking: Users can specify a location for scrap orders, enabling better management and tracking of product waste.
    - Real-time Inventory Updates: Once scrap orders are confirmed, the on-hand quantities are updated in real-time, ensuring accurate stock levels.
    - Detailed Scrap Orders: The app generates detailed scrap orders that users can review and manage, providing full visibility into scrap activity.
    - Scrap Quantity Flexibility: Users can specify the exact number of products to scrap and update the system accordingly, providing flexibility in scrap management.
    - Scrap Order Reporting: All scrap orders are tracked and visible in a dedicated view, offering insights into the amount of product waste and enabling businesses to manage their inventory more effectively.

    How It Works:
    1. Navigate to Inventory -> Products -> Product Variants to access the product variants form view.
    2. Click on the "On Hand" smart button to view and update product quantities. The scrap product functionality will also be available.
    3. When creating a scrap order, specify the scrap quantity and scrap location in the pop-up view.
    4. After confirming the scrap order, the on-hand quantity for the product is updated in the system, reflecting the changes in inventory.
    5. Use the Scrap Orders view (Inventory -> Operations -> Scrap) to track all scrap orders and review product waste.

    This app is ideal for businesses that need to handle product scrap efficiently. It provides easy tracking of scrap quantities, precise location management, and seamless integration into inventory management, ensuring accurate stock levels and reducing unnecessary losses.

    Benefits:
    - Efficient scrap management directly from product variants.
    - Track scrap quantities and locations in real-time.
    - Automatically update inventory after scrap orders are confirmed.
    - Improve product waste management with detailed reports and tracking.
    - Easy-to-use interface for quick access to scrap functionality.

    For more information, support, or a demo, visit our website at https://inkerp.com or contact us via email at team@inkerp.com.
    """,
    'author': "INKERP",
    'website': 'https://www.inkerp.com/',
    "depends": ["product", "stock"],
    "data": ["security/ir.model.access.csv",
             "wizards/product_scrap_wizard_view.xml",
             "views/product_product_view.xml"],
    'images': ['static/description/banner.gif'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
