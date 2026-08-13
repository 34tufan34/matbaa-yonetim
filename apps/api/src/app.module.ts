import { Module } from '@nestjs/common';
import { PrismaModule } from './prisma/prisma.module';
import { HealthModule } from './modules/health/health.module';
import { SystemSettingsModule } from './modules/system-settings/system-settings.module';
import { AuditModule } from './modules/audit/audit.module';

@Module({
  imports: [PrismaModule, HealthModule, SystemSettingsModule, AuditModule],
})
export class AppModule {}
