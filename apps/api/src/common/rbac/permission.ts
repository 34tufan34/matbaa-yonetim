export const Permission = {
  SettingsRead: 'settings.read',
  SettingsWrite: 'settings.write',
  UsersRead: 'users.read',
  UsersWrite: 'users.write',
  RolesManage: 'roles.manage',
  AuditRead: 'audit.read',
  ProductionStart: 'production.start',
  ProductionStop: 'production.stop',
  QualityApprove: 'quality.approve',
  ShipmentApprove: 'shipment.approve',
  MaintenanceManage: 'maintenance.manage',
} as const;

export type PermissionCode = (typeof Permission)[keyof typeof Permission];
