import { Controller, Get, Module } from '@nestjs/common';

@Controller('health')
class HealthController {
  @Get()
  getHealth() {
    return { status: 'ok', service: 'matbaa-api', version: '0.1.0' };
  }
}

@Module({ controllers: [HealthController] })
export class HealthModule {}
