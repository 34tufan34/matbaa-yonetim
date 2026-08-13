import { Controller, Get, Param } from '@nestjs/common';
import { SystemSettingsService } from './system-settings.service';

@Controller('organizations/:organizationId/settings')
export class SystemSettingsController {
  constructor(private readonly service: SystemSettingsService) {}

  @Get()
  list(@Param('organizationId') organizationId: string) {
    return this.service.list(organizationId);
  }

  @Get('dictionaries')
  listDictionaries(@Param('organizationId') organizationId: string) {
    return this.service.listDictionaries(organizationId);
  }
}
