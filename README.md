# Azure Automatic Image Processor

This Azure Function watches the `original-images` Blob container through Event Grid. Each uploaded JPEG or PNG is resized to fit within 800 x 800 pixels while preserving its aspect ratio, then saved under the same filename in `processed-images`.

## Azure resources used

- Storage account: `malarimageproc913`
- Input container: `original-images`
- Output container: `processed-images`
- Function App: `malar-imageprocessor-func913`
- Trigger source: Event Grid

## Deploy from Azure Cloud Shell

Upload `azure-image-processor.zip` to Cloud Shell, then run:

```bash
az functionapp deployment source config-zip \
  --resource-group malar-imageprocessor-func913_group \
  --name malar-imageprocessor-func913 \
  --src azure-image-processor.zip \
  --build-remote true
```

After deployment, refresh the Function App's Functions page and verify that `ProcessUploadedImage` is listed.
