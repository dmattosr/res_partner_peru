# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning

import requests


def get_data_doc_number(tipo_doc, numero_doc, format='json'):
    user, password = 'demorest', 'demo1234'
    url = 'http://py-devs.com/api'
    url = '%s/%s/%s' % (url, tipo_doc, str(numero_doc))
    res = {'error': True, 'message': None, 'data': {}}
    try:
        response = requests.get(url, auth=(user, password))
    except requests.exceptions.ConnectionError:
        res['message'] = 'Error en la conexion'
        return res

    if response.status_code == 200:
        res['error'] = False
        res['data'] = response.json()
    else:
        try:
            res['message'] = response.json()['detail']
        except Exception:
            res['error'] = True
    return res


class ResPartner(models.Model):
    _inherit = "res.partner"

    workplace = fields.Char('Centro de Trabajo')
    doc_type = fields.Selection(
        string='Tipo de Documento',
        selection=(
            ('dni', 'D.N.I.'),
            ('ruc', 'R.U.C.'),
            ('passport', 'Pasaporte'),
            ('other', 'Otro'),
        ),
        default='dni',
    )
    doc_number = fields.Char('Número de Documento')
    country_id = fields.Many2one(
        'res.country',
        default=lambda self: self.env['res.country'].search([('name', '=', 'Perú')]))

    # # sunat
    tipo_contribuyente = fields.Char('Tipo de contribuyente', readonly=True)
    nombre_comercial = fields.Char('Nombre comercial', readonly=True)
    fecha_inscripcion = fields.Date('Fecha de inscripción', readonly=True)
    estado_contribuyente = fields.Char(
        'Estado del contribuyente', readonly=True)
    condicion_contribuyente = fields.Char(
        'Condición del contribuyente', readonly=True)

    agente_retencion = fields.Boolean('Agente de Retención', readonly=True)
    agente_retencion_apartir_del = fields.Date('A partir del', readonly=True)
    agente_retencion_resolucion = fields.Char('Resolución', readonly=True)

    sistema_emision_comprobante = fields.Char('Sistema emisión', readonly=True)
    sistema_contabilidad = fields.Char('Sistema contabilidad', readonly=True)

    ultima_actualizacion_sunat = fields.Date(
        'Última actualización', readonly=True)
    representante_legal_ids = fields.One2many(
        'res.partner.representante_legal', inverse_name='parent_id', readonly=True)

    @api.multi
    def onchange_type(self, is_company):
        res = super(ResPartner, self).onchange_type(is_company)

        if 'value' in res.keys():
            doc_type = is_company and 'ruc' or 'dni'
            res['value'].update({'doc_type': doc_type})

        return res

    @api.onchange('doc_number')
    def onchange_doc_number(self):
        self.button_update_document()

    @api.one
    def button_update_document(self):
        if self.country_id.name == u'Perú':
            if self.doc_type and self.doc_type == 'dni' and \
               not self.is_company:
                if self.doc_number and len(self.doc_number) != 8:
                    raise Warning('El Dni debe tener 8 caracteres')
                else:
                    d = get_data_doc_number(
                        'dni', self.doc_number, format='json')
                    if not d['error']:
                        d = d['data']
                        self.name = '%s %s, %s' % (d['ape_paterno'],
                                                   d['ape_materno'],
                                                   d['nombres'])

            elif self.doc_type and self.doc_type == 'ruc' and \
                    self.is_company:
                if self.doc_number and len(self.doc_number) != 11:
                    raise Warning('El Ruc debe tener 11 caracteres')
                else:
                    d = get_data_doc_number(
                        'ruc', self.doc_number, format='json')
                    if d['error']:
                        return True
                    d = d['data']
                    self.name = d['nombre']
                    self.street = d['domicilio_fiscal']
                    self.street2 = '/'.join((d['departamento'],
                                             d['provincia'],
                                             d['distrito']))
                    self.tipo_contribuyente = d['tipo_contribuyente']
                    self.nombre_comercial = d['nombre_comercial']
                    self.fecha_inscripcion = d['fecha_inscripcion']
                    self.estado_contribuyente = d['estado_contribuyente']
                    self.condicion_contribuyente = d[
                        'condicion_contribuyente']

                    self.agente_retencion = d['agente_retencion']
                    self.agente_retencion_apartir_del = d[
                        'agente_retencion_apartir_del']
                    self.agente_retencion_resolucion = d[
                        'agente_retencion_resolucion']
                    self.ultima_actualizacion_sunat = d[
                        'ultima_actualizacion']
                    self.sistema_emision_comprobante = d[
                        'sistema_emision_comprobante']
                    self.sistema_contabilidad = d[
                        'sistema_contabilidad']

                    self.representante_legal_ids.unlink()
                    for t in d['representantes_legales']:
                        values = dict(
                            parent_id=self.id,
                            documento=t['documento'],
                            nro_documento=t['nro_documento'],
                            nombre=t['nombre'],
                            cargo=t['cargo'],
                            fecha_desde=t['fecha_desde'],
                        )
                        self.representante_legal_ids.create(values)


class res_partner_representante_legal(models.Model):
    _name = 'res.partner.representante_legal'
    _rec_name = 'nombre'

    parent_id = fields.Many2one('res.partner', readonly=True)
    documento = fields.Char('Documento', readonly=True)
    nro_documento = fields.Char('Número', readonly=True)
    nombre = fields.Char('Nombre', readonly=True)
    cargo = fields.Char('Cargo', readonly=True)
    fecha_desde = fields.Date('Cargo desde', readonly=True)
