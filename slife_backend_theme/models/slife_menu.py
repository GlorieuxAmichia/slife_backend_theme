# -*- coding: utf-8 -*-
import logging
import operator
import json
from odoo.http import request
from odoo import models, fields, api, tools, _
from odoo.tools import convert

_logger = logging.getLogger(__name__)

class IrUiMenu(models.Model):
	_inherit = 'ir.ui.menu'

	use_font_icon = fields.Boolean("Use Font Icon", compute='_compute_use_font_icon')

	def _compute_use_font_icon(self):
		for record in self:
			record.use_font_icon = self.env['res.config.settings'].default_get('default_use_font_icon').get('default_use_font_icon')


class Http(models.AbstractModel):
	_inherit = 'ir.http'

	def webclient_rendering_context(self):
		res_config = request.env['res.config.settings'].default_get('default_use_font_icon')
		return {
			'menu_data': request.env['ir.ui.menu'].load_menus(request.debug),
			'session_info': json.dumps(self.session_info()),
			'use_font_icon': request.env['res.config.settings'].default_get('default_use_font_icon').get('default_use_font_icon') ,
		}

# class XmlImport(convert.xml_import):
#
# 	def _tag_menuitem(self, rec, data_node=None, mode=None):
# 		_logger.critical('Nous passons ici ici ici')
# 		rec_id = rec.get("id")
# 		self._test_xml_id(rec_id)
#
# 		# The parent attribute was specified, if non-empty determine its ID, otherwise
# 		# explicitly make a top-level menu
# 		if rec.get('parent'):
# 			menu_parent_id = self.id_get(rec.get('parent',''))
# 		else:
# 			# we get here with <menuitem parent="">, explicit clear of parent, or
# 			# if no parent attribute at all but menu name is not a menu path
# 			menu_parent_id = False
# 		values = {'parent_id': menu_parent_id}
# 		if rec.get('name'):
# 			values['name'] = rec.get('name')
# 		try:
# 			res = [ self.id_get(rec.get('id','')) ]
# 		except:
# 			res = None
#
# 		if rec.get('action'):
# 			a_action = rec.get('action')
#
# 			# determine the type of action
# 			action_type, action_id = self.model_id_get(a_action)
# 			action_type = action_type.split('.')[-1] # keep only type part
# 			values['action'] = "ir.actions.%s,%d" % (action_type, action_id)
#
# 			if not values.get('name') and action_type in ('act_window', 'wizard', 'url', 'client', 'server'):
# 				a_table = 'ir_act_%s' % action_type.replace('act_', '')
# 				self.cr.execute('select name from "%s" where id=%%s' % a_table, (int(action_id),))
# 				resw = self.cr.fetchone()
# 				if resw:
# 					values['name'] = resw[0]
#
# 		if not values.get('name'):
# 			# ensure menu has a name
# 			values['name'] = rec_id or '?'
#
# 		if rec.get('sequence'):
# 			values['sequence'] = int(rec.get('sequence'))
#
# 		values['active'] = self.nodeattr2bool(rec, 'active', default=True)
#
# 		if rec.get('groups'):
# 			g_names = rec.get('groups','').split(',')
# 			groups_value = []
# 			for group in g_names:
# 				if group.startswith('-'):
# 					group_id = self.id_get(group[1:])
# 					groups_value.append((3, group_id))
# 				else:
# 					group_id = self.id_get(group)
# 					groups_value.append((4, group_id))
# 			values['groups_id'] = groups_value
#
# 		# if not values.get('parent_id'):
# 		if rec.get('web_icon'):
# 			values['web_icon'] = rec.get('web_icon')
#
# 		pid = self.env['ir.model.data']._update('ir.ui.menu', self.module, values, rec_id, noupdate=self.isnoupdate(data_node), mode=self.mode, res_id=res and res[0] or False)
#
# 		if rec_id and pid:
# 			self.idref[rec_id] = int(pid)
#
# 		return 'ir.ui.menu', pid
#
#
# 	def __init__(self, cr, module, idref, mode, report=None, noupdate=False, xml_filename=None):
# 		super(XmlImport, self).__init__(cr, module, idref, mode, report=report, noupdate=noupdate, xml_filename=xml_filename)
# 		self._tags['menuitem'] = self._tag_menuitem
