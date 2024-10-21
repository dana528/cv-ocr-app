import {
  Controller,
  Post,
  UploadedFile,
  UseInterceptors,
  Res,
  Body,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import { extname } from 'path';
import axios from 'axios';
import { Response } from 'express';
import * as fs from 'fs';

@Controller('upload')
export class UploadController {
  private flaskEndpointMap = {
    DL: 'http://localhost:5000/process',  
    Passport: 'http://localhost:5000/process'
  };
  

  @Post()
  @UseInterceptors(
    FileInterceptor('image', {
      storage: diskStorage({
        destination: './uploads',
        filename: (req, file, callback) => {
          const fileExtName = extname(file.originalname);
          const randomName = Array(16)
            .fill(null)
            .map(() => Math.round(Math.random() * 16).toString(16))
            .join('');
          callback(null, `${randomName}${fileExtName}`);
        },
      }),
    }),
  )

  async uploadFile(
    @UploadedFile() file: Express.Multer.File,
    @Res() res: Response,
    @Body() body: any,
) {
    try {
        console.log('File uploaded:', file);
        console.log('Received body:', body);
        
        const { docType } = body;
        if (!docType) {
            console.error('Error: Missing document type (docType)');
            return res.status(400).json({ message: 'Missing document type (docType)' });
        }

        const filePath = `./uploads/${file.filename}`;
        console.log('File path for processing:', filePath);
        console.log('File exists:', fs.existsSync(filePath));

        // Read file
        const imageBuffer = fs.readFileSync(filePath);
        const base64Image = imageBuffer.toString('base64');
        console.log('Base64 image length:', base64Image.length);

        const pythonServiceUrl = this.flaskEndpointMap[docType];
        if (!pythonServiceUrl) {
            console.error('Error: Invalid document type:', docType);
            return res.status(400).json({ message: 'Invalid document type' });
        }

        console.log('Sending request to Flask service:', {
            url: pythonServiceUrl,
            data: { image: base64Image , docType},
        });

        const flaskResponse = await axios.post(pythonServiceUrl, { 
          image: base64Image,
          docType 
        });
        console.log('Flask response:', flaskResponse.data);

        fs.unlinkSync(filePath); // Cleanup the uploaded file
        return res.json(flaskResponse.data);
    } catch (error) {
        console.error('Error details:', error);
        if (error.response) {
            console.error('Flask response error:', error.response.data);
            console.error('Flask response status:', error.response.status);
            return res.status(500).json({
                message: 'Error processing image',
                errorDetails: error.response.data,
            });
        }
        console.error('Unexpected error:', error.message);
        console.error('Error stack:', error.stack);
        return res.status(500).json({
            message: 'Error processing image',
            errorDetails: error.message,
        });
    }
}

}
