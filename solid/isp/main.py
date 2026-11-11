from manager import ContentManager, WarehouseWorker


if __name__ == '__main__':
    content_manager = ContentManager()
    content_manager.update_product_catalog()

    warehouse_worker = WarehouseWorker()
    warehouse_worker.manage_inventory()