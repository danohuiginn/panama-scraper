import codecs
import cStringIO
import csv
from datamodel import *
class UnicodeCSVWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    see http://www.python.org/doc/2.5.2/lib/csv-examples.html
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f

    def writerow(self, row):
        self.writer.writerow([codecs.encode(s, 'utf-8') for s in row])
        data = self.queue.getvalue()
        self.stream.write(unicode(data, 'utf-8'))
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def rough_guide():
    f = codecs.open('/tmp/panamacsv', 'w', 'utf-8')
    writer = UnicodeCSVWriter(f)

    allpersons = Person.select()[100000:150000] 
    for person in allpersons:
        row = [person.name]
        relatedcompanies = set()
        for linktype in person.agencys, person.directorships, person.subscriberships:
            for x in linktype:
                relatedcompanies.add(x.name)
                if len(relatedcompanies) > 200:
                    break
        rclist = list(relatedcompanies)
        rclist.sort()
        writer.writerow(row + rclist)

def person_dump():
    f = codecs.open('/tmp/persontable.csv', 'w', 'utf-8')
    writer = UnicodeCSVWriter(f)
    count = 0
    print('dumping persons')
    for person in Person.select().lazyIter():
        writer.writerow([str(person.id), person.name])
        count += 1
        if count % 1000 == 0:
            print(count)
    f.close()

def company_dump():
    f = codecs.open('/tmp/companytable.csv', 'w', 'utf-8')
    writer = UnicodeCSVWriter(f)
    count = 0
    for company in Company.select().lazyIter()[:1000]:
        writer.writerow([str(company.id), company.name, unicode(company.recordid), unicode(company.registerdate)])
        count += 1
        if count % 1000 == 0:
            print(count)
    f.close()


if __name__ == '__main__':
    #person_dump()
    #print('dumped people')
    company_dump()
