from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

print('test')

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = "short_name"
    _sql_constraints = [
        ('name_uniq','UNIQUE (name)', 'Book title must be unique')
    ]
    name = fields.Char('Title', required=True)
    short_name = fields.Char(
        string='Short Title',
        size=100,
        translate=False
        )
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many(
        'res.partner',
        string = 'Authors'
    )
    notes = fields.Text('Internal notes')
    state = fields.Selection(
        [
            ('draft', 'Not available'),
            ('available', 'Available'),
            ('lost', 'Lost')
        ],
        'State' 
    )
    description = fields.Html(
        string='Description',
        sanitize=True,
        strip_style=False,
        translate=False
        )
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print ?')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'lost': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False
        )
    reader_rating = fields.Float(
        'Reader Average Rating',
        digits = (14,4)
    )
    cost_price = fields.Float(
        'Book Cost',
        dp.get_precision('Book Price')
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency' 
    )
    retail_price = fields.Monetary(
        'Retail Price',
        currency_field='currency_id'
    )
    publisher_id = fields.Many2one(
        'res.partner',
        string="Publisher",
        ondelete="set null",
        context={},
        domain=[]
    )

    @api.constrains('date_release')
    def _check_release_date(self):
        for record in self:
            if record.date_release and record.date_release > fields.Date.today():
                raise models.ValidationError('Release date must be in the past')

class ResPartner(models.Model):
    _inherit = "res.partner",
    published_book_ids = fields.One2many(
        'library.book',
        'publisher_id',
        string="Published Books"
    )
    authored_book_ids = fields.Many2many(
        'library.book',
        string="Authored Books",
        relation="library_book_res_partner_rel"
    )