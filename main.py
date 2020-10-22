#criador de massa para testar a contabilidade
import uuid
import csv
from datetime import date, timedelta
from faker import Faker

fake = Faker(['pt-BR'])
Faker.seed(0)

adquirentes = ['Rede','Global']
bandeiras = ['Mastercard','Visa','Hiper','Elo']
naturezas = ['credito','debito','parcelado']

taxa_mdr_debito = 1/100
taxa_mdr_credito = 1.99/100
taxa_mdr_parcelado_6 = 2.39/100
taxa_mdr_parcelado_6_mais = 2.69/100

taxa_mdr_adq_debito = 0.5/100
taxa_mdr_adq_credito = 0.9/100
taxa_mdr_adq_parcelado_6 = 1.76/100
taxa_mdr_adq_parcelado_6_mais = 1.99/100

class Transacao:
    def clone(self, tran):
        self.dt_tran = tran.dt_tran
        self.dt_pag = tran.dt_pag
        self.dt_pag_prev = tran.dt_pag_prev
        self.numUnico = str(uuid.uuid1())
        self.nsu = tran.nsu
        self.cnpj = tran.cnpj
        self.adquirente = tran.adquirente
        self.bandeira = tran.bandeira
        self.natureza = tran.natureza
        self.valor_bruto = tran.valor_bruto
        self.valor_liquido = tran.valor_liquido
        self.mdr = tran.mdr
        self.mdr_adq = tran.mdr_adq
        self.resultado = tran.resultado
        self.tot_parcelas = tran.tot_parcelas
        self.numParcela = tran.numParcela
        self.antecipado = tran.antecipado

        return self

    def __init__(self):
        self.dt_tran=date.today()
        self.dt_pag=date.today()
        self.dt_pag_prev=''
        self.numUnico=str(uuid.uuid1())
        self.nsu = 0
        self.cnpj=''
        self.adquirente = ''
        self.bandeira=''
        self.natureza=''
        self.valor_bruto = 0
        self.valor_liquido = 0
        self.mdr = 0
        self.mdr_adq = 0
        self.resultado = 0
        self.tot_parcelas = 0
        self.numParcela = 0
        self.antecipado = 0

    def row(self):
        arr = [ self.dt_tran,
                self.dt_pag_prev,
                self.dt_pag,
                self.numUnico,
                '="'+self.nsu+'"',
                self.cnpj,
                self.adquirente,
                self.bandeira,
                self.natureza,
                self.valor_bruto,
                self.valor_liquido,
                self.mdr,
                self.mdr_adq,
                self.resultado,
                self.tot_parcelas,
                self.numParcela,
                self.antecipado]
        return arr

    def print(self,pretty):
        str = """
            self.dt_tran={0},
            self.dt_pag_prev={1}
            self.dt_pag={2},
            self.numUnico={3},
            self.nsu={4},
            self.cnpj={5},
            self.adquirente={6},
            self.bandeira={7},
            self.natureza={8},
            self.valor_bruto={9},
            self.valor_liquido={10},
            self.mdr={11},
            self.mdr_adq={12},
            self.resultado={13},
            self.tot_parcelas={14},
            self.numParcela={15},
            self.antecipado={16}
            """.format( \
            self.dt_tran,
            self.dt_pag_prev,
            self.dt_pag,
            self.nsu,
            self.numUnico,
            self.cnpj,
            self.adquirente,
            self.bandeira,
            self.natureza,
            self.valor_bruto,
            self.valor_liquido,
            self.mdr,
            self.mdr_adq,
            self.resultado,
            self.tot_parcelas,
            self.numParcela,
            self.antecipado
             )

        #print(str)

class randomTran:
    def randomTran(self, tran):
        trans=[]

        tot_parcelas = fake.random_int(2, 12)

        tran.numUnico = str(uuid.uuid1())
        tran.nsu = str(fake.random_int(1000, 100000)) + str(fake.random_int(1000, 100000)) + str(fake.random_int(1000, 100000))

        tran.cnpj= fake.random_int()

        tran.adquirente= adquirentes[fake.random_int(0, len(adquirentes)-1 )]
        tran.natureza = naturezas[fake.random_int(0, len(naturezas)-1 )]
        tran.bandeira = bandeiras[fake.random_int(0, len(bandeiras)-1 )]

        tran.tot_parcelas = 0

        valor = fake.random_int(0, 1000) + fake.random_int(0, 99)/100
        tran.valor_bruto = round(valor, 2)

        if tran.natureza == 'debito':
            tran.mdr = round(tran.valor_bruto * taxa_mdr_debito, 2)
            tran.mdr_adq = round(tran.valor_bruto * taxa_mdr_adq_debito, 2)
        elif tran.natureza == 'credito':
            tran.mdr = round(tran.valor_bruto * taxa_mdr_credito, 2)
            tran.mdr_adq = round(tran.valor_bruto * taxa_mdr_adq_credito, 2)
        elif tran.natureza == 'parcelado':
            if tot_parcelas <= 6:
                tran.mdr = round(tran.valor_bruto * taxa_mdr_parcelado_6, 2)
                tran.mdr_adq = round(tran.valor_bruto * taxa_mdr_adq_parcelado_6, 2)
            else:
                tran.mdr = round(tran.valor_bruto * taxa_mdr_parcelado_6_mais, 2)
                tran.mdr_adq = round(tran.valor_bruto * taxa_mdr_adq_parcelado_6_mais, 2)

        tran.valor_liquido = round(tran.valor_bruto - tran.mdr, 2)
        tran.resultado = round(tran.mdr - tran.mdr_adq,2)

        rdate_init = fake.random_int(0, 365)
        rdate_end = rdate_init + (30 * fake.random_int(0, 12))
        menos_mais = fake.random_int(0, 100000)
        menos_mais = (menos_mais / 100000)*100
        #print(menos_mais)
        antecipado = 0

        futuro = 0
        sinal='+'
        if menos_mais < 50:
            sinal = '-'
            antecipado = 1

        if futuro == 0:
            sinal = '-'

        init_date_str = str(sinal + str(rdate_init) + 'd')
        end_date_str = str('+' + str(rdate_end) + 'd')

        if futuro == 0:
            end_date_str = 'today'

        #print(init_date_str)
        #print(end_date_str)

        tran.dt_tran = fake.date_between(start_date=init_date_str, end_date=end_date_str)
        #print(tran.dt_tran)

        if tran.natureza == 'debito':
            tran.dt_pag = tran.dt_tran + timedelta(days=1)
            tran.dt_pag_prev = tran.dt_pag
            if tran.dt_pag > date.today():
                tran.dt_pag = ''
            tran.numParcela = 1
            trans.append(tran)
        elif tran.natureza == 'credito':
            tran.numParcela = 1
            tran.dt_pag = tran.dt_tran + timedelta(days=30)
            tran.dt_pag_prev = tran.dt_pag
            if tran.dt_pag > date.today():
                tran.dt_pag = ''
            trans.append(tran)
        elif tran.natureza == 'parcelado':
            tran.tot_parcelas = tot_parcelas
            for i in range(tran.tot_parcelas):
                pTran = Transacao()
                pTran = pTran.clone(tran)
                pTran.numParcela = i+1
                pTran.dt_pag = tran.dt_tran + timedelta(days=30 * pTran.numParcela)
                pTran.dt_pag_prev = pTran.dt_pag
                if antecipado == 1:
                    pTran.antecipado = 1
                    pTran.dt_pag = tran.dt_tran
                elif pTran.dt_pag > date.today():
                        pTran.dt_pag = ''
                trans.append(pTran)
        return trans

def localize_floats(row):
    return [
        str(el).replace('.', ',') if isinstance(el, float) else el
        for el in row
    ]

def main():
    r = randomTran()
    with open('transacoes-' + str(uuid.uuid1()) + '.csv', mode='w') as csv_file:
        fieldnames = ['data transacao', 'data pagamento prevista', 'data pagamento', 'numero unico', 'nsu', 'cnpj', 'adquirente', 'bandeira', 'natureza',
                      'valor bruto', 'valor liquido', 'mdr', 'mdr adquirente', 'resultado',
                      'total parcelas', 'numero parcela', 'antecipada']
        write = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        write.writerow(fieldnames)
        for i in range(1000):
            t = Transacao()
            trans = r.randomTran(t)
            for l in trans:
                write.writerow(localize_floats(l.row()))

if __name__ == "__main__":
    main()
