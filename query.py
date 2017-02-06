"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?
# It's a query object, not an actual query yet (we need to add .all() or .one(),
# etc)



# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?
# An association table is used to manage many to many relationships, or really,
# two one-to-many relationships.  We use the term to distinguish it from a
# middle table, which has meaningful data fields, in addition to the foreign
# keys.  We would use a middle table to store book comments by users, because a
# book can have many comments and a user can make many comments, and a user can
# make multiple comments for the same book.  So the middle table stores
# commentid, userid, bookid, comment.
# An association table is used to connect two other tables that don't really
# have a direct relationship, and would be used when we don't have meaningful
# data to store, aside from the foreign keys.  Ex: a book can have many genres,
# and a genre can have many books, but we don't really have any other
# information to store about bookgenres.  We would have an association table,
# with bookgenreid, bookid, genreid, and that's it.




# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the ``id`` of "ram."
q1 = db.session.query(Brand).filter(Brand.brand_id == "ram").first()

# Get all models with the name "Corvette" and the brand_id "che."
q2 = db.session.query(Model).filter(Model.name == "Corvette",
                                    Model.brand_id == "che").all()

# Get all models that are older than 1960.
q3 = db.session.query(Model).filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = db.session.query(Brand).filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor."
q5 = db.session.query(Model).filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = db.session.query(Brand).filter(Brand.founded == 1903,
                                    Brand.discontinued.is_(None)).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = db.session.query(Brand).filter((Brand.discontinued.isnot(None)) |
                                    (Brand.founded < 1950)).all()

# Get any model whose brand_id is not "for."
q8 = db.session.query(Model).join(Brand).filter(Brand.brand_id != 'for').all()

# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    # yearcars = db.session.query(Model).join(Brand).filter(Model.year == year).all()
    # for model, brand in yearcars:
    #     print model.name, brand.name, brand.headquarters
    yearcars = Model.query.options(db.joinedload('brand')).filter_by(year=year).all()

    for yearcar in yearcars:
        print "Model: %s \nBrand: %s\nHeadquarters: %s\n" % (yearcar.name,
                                                             yearcar.brand.name,
                                                             yearcar.brand.headquarters
                                                             )


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query."""

    brndmdls = Brand.query.options(db.joinedload('model')).all()

    for brnd in brndmdls:
        print "Brand: %s" % (brnd.name)
        for mdl in brnd.model:
            print "      Model: %s\n      Year: %s\n" % (mdl.name, mdl.year)


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    return Brand.query.filter(Brand.name.like('%'+mystr+'%')).all()


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year,
                              Model.year < end_year).all()
