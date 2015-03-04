### encoding: utf8 ###
from django.db import models

INFLATION = {1992: 2.338071159424868,
 1993: 2.1016785142253185,
 1994: 1.8362890269054741,
 1995: 1.698638328862775,
 1996: 1.5360153664058611,
 1997: 1.4356877762122495,
 1998: 1.3217305991625745,
 1999: 1.3042057718241757,
 2000: 1.3042057718241757,
 2001: 1.2860800081392196,
 2002: 1.2076314957018655,
 2003: 1.2308469660644752,
 2004: 1.2161648953888384,
 2005: 1.1878270593983091,
 2006: 1.1889814138002117,
 2007: 1.1499242230869946,
 2008: 1.1077747422214268,
 2009: 1.0660427753379829,
 2010: 1.0384046275616676,
 2011: 1.0163461588107117,
 2012: 1.0,
 2013: 1.0,
 2014: 1.0,
}

class BudgetLine(models.Model):
    
    name                = models.CharField( max_length=256, db_index=True )
    budget_id           = models.CharField( max_length=64,db_index=True )
    parent              = models.ForeignKey( 'self', related_name='sublines', null=True, db_index=True )
    amount              = models.PositiveIntegerField( db_index=True ) # TODO: Not int?    
    year                = models.PositiveIntegerField( db_index=True )
    
    
    # TODO: More fields?
    
    @property
    def inflation_factor(self): return INFLATION.get(self.year, 1)
