import dataset
import sqlalchemy


def setup():
    db = dataset.connect('postgresql+psycopg2://postgres@localhost/legendastvmirror')
    table = db.get_table('shows')
    table.create_column('exists', sqlalchemy.Boolean)
    table.create_column('show_id', sqlalchemy.Integer)
    table.create_column('last_change_time', sqlalchemy.DateTime)
    table.create_column('show_name', sqlalchemy.String(200, convert_unicode=True))
    table.create_column('status', sqlalchemy.String(20))
    table.create_index(['show_id'])

    table = db.get_table('releases')
    table.create_column('status', sqlalchemy.String(20))
    table.create_column('language', sqlalchemy.String(20))
    table.create_column('release_link', sqlalchemy.String(4000))
    table.create_column('show_id', sqlalchemy.Integer)
    table.create_column('subtitle_download_link', sqlalchemy.String(4000))
    table.create_column('last_change_time', sqlalchemy.DateTime)
    table.create_column('filename', sqlalchemy.String(4000))
    table.create_column('slug', sqlalchemy.String(4000))

if __name__ == '__main__':
    setup()
