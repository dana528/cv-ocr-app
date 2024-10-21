import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { join } from 'path';
import { NestExpressApplication } from '@nestjs/platform-express';

async function bootstrap() {
  const app = await NestFactory.create<NestExpressApplication>(AppModule);

  // erve the static HTML upload form
  app.useStaticAssets(join(__dirname, '..', 'uploads'));
  
  await app.listen(3000);
  console.log('Server running on http://localhost:3000');
}
bootstrap();
