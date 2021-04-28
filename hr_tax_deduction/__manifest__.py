# -*- coding: utf-8 -*-
{'name': "Employee  tax_deductions ",
 'summary': """
       Multiple tax_deductions for employee""",
 'description': """
            Add many tax_deductions to any employee, include in payroll and END of Service Reward calculation
    """,
 'author': "I VALUE solutions",
 'website': "https://www.anviz.com",
 'email': "info@anviz.com",
 'license': "OPL-1",
 'category': 'HR',
 'version': '0.1',
 'images': [],
 'depends': ['base', 'mail', 'hr', ],
 'data': [
     'data/data.xml',
     'security/hr_tax_deduction_security.xml',
     'security/ir.model.access.csv',
     'views/hr_tax_deduction_views.xml',
 ],
 'demo': []
 }
