# Planlanan veri modeli

## Platform
organization, facility, user, role, permission, user_role, role_permission, app_setting, system_dictionary, system_dictionary_item, audit_log, device, sync_mutation, notification_rule, notification, file_asset, entity_file.

## İnsan ve vardiya
employee, employee_skill, machine_qualification, training, certificate, leave_record, absence_record, shift_definition, shift_instance, shift_assignment, shift_handover.

## Ticari ve ürün
customer, customer_contact, customer_instruction, customer_complaint, quotation, sales_order, sales_order_line, product, product_revision, product_attribute, production_route, route_operation, work_order.

## Üretim
production_plan, plan_operation, production_run, production_event, production_counter, downtime_event, downtime_reason, scrap_event, scrap_reason, operation_assignment.

## Kalite
quality_template, quality_template_field, quality_rule, quality_inspection, quality_result, nonconformance, nonconformance_action, approval.

## Makine ve bakım
machine, machine_capability, machine_state_event, meter_reading, maintenance_plan, maintenance_work_order, breakdown, breakdown_action, spare_part, machine_spare_part, maintenance_part_usage.

## Stok ve satın alma
warehouse, bin_location, material, inventory_lot, stock_movement, stock_reservation, supplier, purchase_request, purchase_request_line, purchase_order, goods_receipt.

## Sevkiyat ve maliyet
packing_unit, shipment, shipment_line, shipment_check, estimated_cost, actual_cost, cost_line.

## Yönetim
kpi_snapshot, oee_snapshot, command_center_projection, decision_suggestion, report_job.

## İlişki ilkesi
Ana kayıtlar silinmez; `isActive`/durum ile pasifleştirilir. Finansal/üretimsel işlem kayıtlarında hard delete yasaktır. Foreign key ile zincir korunur; serbest metinle makine/personel/müşteri adı saklanmaz.
