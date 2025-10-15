# Direct Video Upload Feature for Home Slider

## Overview
The home slider now supports direct video file uploads (not URLs) with strict validation for 15-second duration limit, allowing administrators to upload video content alongside traditional image slides.

## Features Added

### Backend Changes
1. **HomeSlider Model Updates**:
   - Added `media_type` field (choices: 'image', 'video')
   - Added `video` field for direct video file uploads (not URLs)
   - Added `video_poster` field for video poster images
   - Made `image` field optional (blank=True, null=True)
   - Added `media_url` and `poster_url` properties
   - **Video Validation**: 15-second duration limit, 50MB file size limit, MP4/MOV/AVI formats only

2. **Admin Interface**:
   - Updated admin interface to support video uploads
   - Added media type selection
   - Organized fields into logical sections
   - Added helpful descriptions for video fields

3. **API Serializer**:
   - Updated HomeSliderSerializer to include video fields
   - Added `media_url` and `poster_url` serialized fields
   - Proper URL handling for both images and videos

### Frontend Changes
1. **Hero Component**:
   - Updated to detect and render videos vs images
   - Added video element with autoplay, muted, loop attributes
   - Proper z-index layering for content overlay
   - Fallback to images if video fails to load

2. **CSS Styling**:
   - Added styles for `.hero-video`, `.hero-image`, `.hero-overlay`
   - Proper positioning and z-index management
   - Responsive video display

## How to Use

### For Administrators

1. **Access Admin Panel**:
   - Go to Django admin panel
   - Navigate to "Home Sliders" section

2. **Create New Video Slide**:
   - Click "Add Home Slider"
   - Fill in title and subtitle
   - Select "Video" as media type
   - Upload video file (MP4/MOV/AVI, max 15 seconds, max 50MB)
   - Optionally upload a poster image (shown before video loads)
   - Set button text and URL
   - Set display order and activate

3. **Video Requirements**:
   - **Format**: MP4, MOV, or AVI formats only
   - **Duration**: Maximum 15 seconds (strictly enforced)
   - **File Size**: Maximum 50MB
   - **Resolution**: 1920x1080 or similar for full-screen display
   - **Upload**: Direct file upload only (no URLs)

### For Developers

1. **API Usage**:
   ```javascript
   // Fetch slider data
   const response = await apiService.getHomeSliders();
   const slides = response.data;
   
   // Check media type
   slides.forEach(slide => {
     if (slide.media_type === 'video') {
       console.log('Video URL:', slide.media_url);
       console.log('Poster URL:', slide.poster_url);
     } else {
       console.log('Image URL:', slide.media_url);
     }
   });
   ```

2. **Frontend Integration**:
   The Hero component automatically handles both media types:
   - Videos are displayed with autoplay, muted, and loop
   - Images are displayed as background images
   - Content overlay ensures text remains readable

## Technical Details

### Database Schema
```sql
-- New fields added to HomeSlider model
media_type VARCHAR(10) DEFAULT 'image'
video VARCHAR(100) NULL
video_poster VARCHAR(100) NULL
image VARCHAR(100) NULL (changed from NOT NULL)
```

### File Storage
- Videos: `media/home_slider/videos/`
- Posters: `media/home_slider/posters/`
- Images: `media/home_slider/` (existing)

### Browser Compatibility
- **Videos**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Fallback**: Images are used if video fails to load
- **Mobile**: Videos use `playsInline` attribute for iOS compatibility

## Performance Considerations

1. **Video Optimization**:
   - Compress videos for web delivery
   - Use appropriate bitrates
   - Consider using WebM format for smaller file sizes

2. **Loading Strategy**:
   - Videos are loaded on-demand
   - Poster images provide immediate visual feedback
   - Lazy loading can be implemented for better performance

3. **Caching**:
   - Video files should be cached by CDN
   - Consider using video streaming services for large files

## Future Enhancements

1. **Video Controls**: Add play/pause controls for user interaction
2. **Multiple Formats**: Support for WebM, OGG video formats
3. **Video Streaming**: Integration with video streaming services
4. **Analytics**: Track video engagement metrics
5. **Responsive Videos**: Different video sizes for different screen sizes

## Troubleshooting

### Common Issues

1. **Video Upload Rejected**:
   - Check video duration (must be ≤ 15 seconds)
   - Check file size (must be ≤ 50MB)
   - Check file format (MP4, MOV, or AVI only)
   - Ensure it's a direct file upload, not a URL

2. **Video Not Playing**:
   - Check file format (MP4 recommended)
   - Verify file size and compression
   - Check browser console for errors

3. **Poster Not Showing**:
   - Ensure poster image is uploaded
   - Check image file format and size

4. **Performance Issues**:
   - Optimize video file size
   - Consider using video compression tools
   - Implement lazy loading for better performance

### Validation Features

1. **Automatic Duration Check**:
   - System automatically validates video duration using OpenCV
   - Videos longer than 15 seconds are rejected with clear error message

2. **File Size Validation**:
   - Maximum 50MB file size limit
   - Clear error message if exceeded

3. **Format Validation**:
   - Only MP4, MOV, and AVI formats accepted
   - Other formats are rejected with helpful error message

### Support
For technical support or questions about this feature, please contact the development team.
