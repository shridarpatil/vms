# Copyright (c) 2022, Shridhar Patil and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class VolCheckin(Document):

	def validate(self):
		activity = frappe.db.get_value(
			"Vol Activity",
			self.activity,
			["start_date", "end_date", "status"],
			as_dict=True
		)
		if activity.status == 'Closed':
			frappe.throw(f"Activity <b>{self.activity}</b> has been closed")

		if activity.start_date and self.date < str(activity.start_date):
			frappe.throw(f"Activity <b>{self.activity}</b> will start on {str(activity.start_date)}")

		if activity.end_date and self.date > str(activity.end_date):
			frappe.throw(f"Activity <b>{self.activity}</b> has been ended on {str(activity.end_date)}")


	def before_insert(self):
		if not self.user:
			self.user = frappe.session.user

		if frappe.local.conf.get("approve_checkin"):
			self.status = "Pending"
		else:
			self.status = "Approved"