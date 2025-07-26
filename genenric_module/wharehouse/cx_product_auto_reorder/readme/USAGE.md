Create new Rule Template

1.  - Go to Inventory
2.  - Select Menu Configuration -\> Reordering Rule Templates
3.  - Select Product Category and/or Product Attribute Values.
4.  - Configure rule settings (min/max qty, warehouse, company etc.).
5.  - Do not forget: Category and Product Attribute Values can be
      specified ONLY when the Template is created!
6.  - Reordering rules will be created automatically for all products
      matching template

Create new Product

1.  - Reordering rules will be created automatically when a product is
      created if product category/attributes match any template
2.  - Check "Don't create reordering rules from templates" if you do not
      want to create Reordering Rules automatically

Reordering Rules Templates are applied to ALL Products EXCEPT for the
ones with "Don't create reordering rules from templates" enabled. When
a new product is created, the first matching template is applied and
reordering rules for the product are created. First matching template is
applied. Templates are searched in the following order: 1. Local
Attributed: Product Attribute Values\* AND Category are matching. [Click
to get Pro
Version!](https://apps.odoo.com/apps/modules/18.0/cx_product_auto_reorder_pro)
2. Local: Category is matching. 3. Global Attributed: Product Attribute
Values\* matching, Category not set. 4. Global: Product Attribute
Values\* and Category are not set.

When product category or attribute values are changed, Reordering Rules
Templates are applied again. In case no new template can be applied, old
reordering rules for the product are deleted.

**\*Hint:**\* to prevent automatic deletion or modification of
reordering rules disable "Control via Template" in Reordering Rule form.

**\*Important notice:**\* The attribute values are joined using the "AND"
statement (e.g. "Size:L" AND "Color:White" AND "Model:Vintage"). It
means that the template will be applied to the product only if 'ALL'
attribute values match.

**Warning! Product Category and Attribute Values cannot be changed once
a template is created!**
