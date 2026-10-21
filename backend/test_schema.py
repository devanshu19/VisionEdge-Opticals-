import os
import sys

# Backup old SQLite
db_path = 'visionedge.db'
if os.path.exists(db_path):
    backup = 'visionedge_backup_pre_migration.db'
    if not os.path.exists(backup):
        os.rename(db_path, backup)
        print(f'Backed up: {db_path} -> {backup}')
    else:
        os.remove(db_path)
        print(f'Removed old {db_path}')

from app import create_app
from models import db
from sqlalchemy import text, inspect

app = create_app()
with app.app_context():
    db.create_all()
    print('PASS: db.create_all()')

    result = db.session.execute(text('SELECT 1'))
    print(f'PASS: SELECT 1 = {result.scalar()}')

    insp = inspect(db.engine)
    tables = sorted(insp.get_table_names())
    print(f'PASS: {len(tables)} tables created: {tables}')

    order_cols = [c['name'] for c in insp.get_columns('order')]
    for col in ['subtotal', 'gst', 'discount', 'priority', 'notes']:
        assert col in order_cols, f'Missing order.{col}'
    print('PASS: Order new columns OK')

    it_cols = [c['name'] for c in insp.get_columns('inventory_transaction')]
    assert 'reference_number' in it_cols, 'Missing reference_number'
    print('PASS: InventoryTransaction.reference_number OK')

    brand_cols = [c['name'] for c in insp.get_columns('brand')]
    assert 'status' in brand_cols
    assert 'logo' in brand_cols
    print('PASS: Brand columns OK')

    cat_cols = [c['name'] for c in insp.get_columns('category')]
    assert 'type' in cat_cols
    print('PASS: Category.type OK')

    print()
    print('=== ALL SCHEMA TESTS PASSED ===')
