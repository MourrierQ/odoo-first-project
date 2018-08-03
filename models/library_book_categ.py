from odoo import models,fields,api

class LibraryBookCateg(models.Model):
    _name ='library.book.category'
    
    #Enables the special hierarchy support
    _parent_store = True
    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    # =====================================
    
    name =fields.Char('Category')
    parent_id = fields.Many2one(
        'library.book.category',
        string="Parent Category",
        ondelete='restrict',
        index=True
    )
    child_ids = fields.One2many(
        'library.book.category',
        'parent_id',
        string="Child Categories"
    )

    #To prevent looping relations:
    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error ! You cannot create recursive categories')
