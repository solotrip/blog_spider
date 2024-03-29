from blog_spider.exporters import JsonLinesGzipItemExporter
from datetime import datetime
from pathlib import Path

class JsonPipeline(object):
    filenames = {}
    exporters = {}
    files = {}

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            output_path=crawler.settings.get('OUTPUT_PATH', 'blog_spider/crawled/'),
        )
    def __init__(self, output_path):
        self.output_path = output_path


    def _create_exporter(self, domain):
        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        folder = Path(self.output_path)
        self.filenames[domain] = folder / "{}_{}.jsonl.gz".format(domain,date)
        self.files[domain] = open(self.filenames[domain], 'wb')
        self.exporters[domain] = JsonLinesGzipItemExporter(self.files[domain], encoding='utf-8', ensure_ascii=False)
        return self.exporters[domain]

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()
        for file in self.files.values():
            file.close()

    def process_item(self, item, spider):
        page = item.get('domain')
        exporter = self.exporters.get(page)
        if not exporter:
            exporter = self._create_exporter(page)
        exporter.export_item(item)
        return item
