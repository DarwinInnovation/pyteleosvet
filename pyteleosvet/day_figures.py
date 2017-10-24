'''
Created on 3 May 2013

@author: richardm
'''
__author__ = 'richardm'

import datetime
from pyteleosvet.model import Transactions
import peewee
from decimal import Decimal

class DayTotal(object):
    def __init__(self, name, dir):
        self._name = name
        self._dir  = dir
        self._exvat = 0
        self._incvat = 0
        self._vat = 0

        self._count = 0

    def set(self, count, exvat, incvat):
        if incvat is None:
            incvat = 0
        if exvat is None:
            exvat = 0

        self._exvat = exvat * self._dir
        self._incvat = incvat * self._dir
        self._vat = (incvat-exvat)\

        if abs(self._vat)>0.005:
            self._vat = self._vat * self._dir

        self._count = count

    def getTableRow(self, mult):
        mult = mult or 1
        return [self._name,
                "&pound;%.2f"%(self._incvat*mult),
                self._count,
                "&pound;%.2f"%(self._exvat*mult)]

    def __add__(self, other):
        total = DayTotal('TOTAL', self._dir)

        total._exvat = self._exvat + other._exvat
        total._incvat = self._incvat + other._incvat
        total._vat = self._vat + other._vat
        total._count = self._count + other._count

        return total

    def __str__(self):
        return "%10s %5d %9.2f %9.2f %9.2f"%(self._name, self._count, self._incvat, self._exvat, self._vat)

oneday = datetime.timedelta(days=1)

class DayFigures(object):
    _payment_types = [
        'Cash', 'Cheque', 'C/Card', 'BACS', 'Voucher'
    ]

    def __init__(self, dt):
        self._date = dt

        self._payments = {}

        self._invoices = DayTotal('Invoice', -1)
        self._credit_notes = DayTotal('Credit', -1)
        for t in DayFigures._payment_types:
            self._payments[t] = DayTotal(t, -1)

    def get(self):
        self._get_invoices()
        self._get_credit_notes()
        for t in DayFigures._payment_types:
            self._get_payments(t)
        return self

    def _get_invoices(self):
        vals = Transactions.select(
            peewee.fn.COUNT(Transactions.net_value).alias('count'),
            peewee.fn.SUM(Transactions.net_value),
            peewee.fn.SUM(Transactions.amount_in_currency)
        ).where(
                (Transactions.invoice_date.between(self._date, self._date + oneday)) &
                (Transactions.procedure == 2) &
                (Transactions.net_value > 0) &
                (Transactions.currency_abbreviation != 'IGN')).get()

        self._invoices.set(vals.count, vals.net_value, vals.amount_in_currency)

        return vals.count

    def _get_credit_notes(self):
        vals = Transactions.select(
            peewee.fn.COUNT(Transactions.net_value).alias('count'),
            peewee.fn.SUM(Transactions.net_value),
            peewee.fn.SUM(Transactions.amount_in_currency)
        ).where(
                (Transactions.invoice_date.between(self._date, self._date + oneday)) &
                (Transactions.procedure == 2) &
                (Transactions.net_value < 0) &
                (Transactions.currency_abbreviation != 'IGN')).get()

        self._credit_notes.set(vals.count, vals.net_value, vals.amount_in_currency)

        return vals.count

    def _get_payments(self, type):
        vals = Transactions.select(
            peewee.fn.COUNT(Transactions.net_value).alias('count'),
            peewee.fn.SUM(Transactions.net_value),
            peewee.fn.SUM(Transactions.amount_in_currency)
        ).where(
            (Transactions.invoice_date.between(self._date, self._date + oneday)) &
            (Transactions.procedure << [8, 9]) &
            (Transactions.details % ('%<' + type + '>%')) &
            (Transactions.currency_abbreviation != 'IGN')).get()

        self._payments[type].set(vals.count, vals.net_value, vals.amount_in_currency)

    def __str__(self):
        s = "Figures for %s\n"%(self._date.strftime("%d/%m/%y"))
        s += "\t%s\n"%self._invoices
        s += "\t%s\n" % self._credit_notes
        s += "="*50+"\n"
        s += "\t%s\n" % (self._invoices + self._credit_notes)
        s += "\n"

        total = DayTotal('Total', 1)
        for t in range(0, len(DayFigures._payment_types)):
            v = DayFigures._payment_types[t]
            s += "\t%s\n"%self._payments[v]
            total += self._payments[v]

        s += "=" * 50 + "\n"
        s += "\t%s\n" % (total)

        return s

    def vt_inv(self, primary_acc):
        invs=self._invoices
        if (abs(invs._incvat) < 0.005):
            return None

        out='SIN,'                                  # Type
        out+='[auto],'                              # Ref no
        out+='%s,'%self._date.strftime("%d/%m/%y")  # Date
        out+='"%s",'%primary_acc                    # Primary account
        out+='"Teleos Invoices (%d)",'%invs._count         # Details
        out+='%.2f,'%(-invs._incvat)                  # Total
        out+='%.2f,'%(-invs._vat)                      # VAT
        out+='%.2f,'%(-invs._exvat)                    # ex VAT
        out+='"Income: Sales",'                     # Analysis account
        out+=',,\n'
        return out

    def vt_cns(self, primary_acc):
        cns=self._credit_notes
        if (abs(cns._incvat) < 0.005):
            return None

        out='SCR,'                                  # Type
        out+='[auto],'                              # Ref no
        out+='%s,'%self._date.strftime("%d/%m/%y")  # Date
        out+='"%s",'%primary_acc                    # Primary account
        out+='"Teleos Credit Notes (%d)",'%cns._count         # Details
        out+='%.2f,'%(cns._incvat)                  # Total
        out+='%.2f,'%(cns._vat)                      # VAT
        out+='%.2f,'%(cns._exvat)                    # ex VAT
        out+='"Income: Sales",'                     # Analysis account
        out+=',,\n'
        return out

    def vt_payments(self, primary_acc, type_map):
        total=Decimal('0.00')
        for t in DayFigures._payment_types:
            total += self._payments[t]._exvat

        if total <= 0:
            return None

        out='JRN,[auto],'
        out+='%s,,"%s",,,'%(self._date.strftime("%d/%m/%y"), "Payments")
        out+='%.2f,"%s","%s",""\n'%(-total,primary_acc,"Teleos Payments Total")

        for t in DayFigures._payment_types:
            dt = self._payments[t]
            if dt._exvat > 0:
                out +='"","","","","",,,%.2f,"%s","%s",\n'%(dt._exvat,type_map['acc']%t,type_map['details']%t)

        return out

    def get_table(self, min_type, max_type, mult):
        mult = mult or 1

        table = []
        total = DayTotal(0, "TOTAL", 1)
        for t in range(min_type, max_type):
            total.add(self._payments[t])
            table.append(self._payments[t].getTableRow(mult))
        table.append(total.getTableRow(mult))
        return table
