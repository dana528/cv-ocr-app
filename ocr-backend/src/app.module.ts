import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { OcrModule } from './ocr/ocr.module';
import { UploadController } from './upload/upload.controller';

@Module({
  imports: [OcrModule],
  controllers: [AppController, UploadController],
  providers: [AppService],
})
export class AppModule {}
