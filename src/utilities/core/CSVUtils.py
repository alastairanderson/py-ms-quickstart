import csv


class CSVUtils:

    @staticmethod
    def read_header(file):
        fields = []
        with open(file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)    
            iter_rows = iter(csvreader)
            fields = next(iter_rows)
        csvfile.close()
        return fields


    @staticmethod
    def read_ordered_header(file):
        result = {}
        with open(file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)    
            iter_rows = iter(csvreader)
            fields = next(iter_rows)
            for i in range(0, len(fields)):
                result[str(i)] = fields[i]
        csvfile.close()
        return result


    @staticmethod
    def read_content(file):
        rows = []
        with open(file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            iter_rows = iter(csvreader)
            fields = next(iter_rows)
            for row in iter_rows:
                rows.append(row)
        csvfile.close()
        return rows


    @staticmethod
    def write(data, file_path):
        file = open(file_path, 'w')
        with file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerows(data)
        file.close()