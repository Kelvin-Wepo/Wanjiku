const theme = {
  colors: {
    primary: '#3B82F6',       // Modern blue
    secondary: '#8B5CF6',     // Purple
    accent: '#10B981',        // Emerald
    background: '#F3F4F6',    // Cool gray
    surface: '#FFFFFF',       // White surface
    text: '#1F2937',         // Dark text
    textLight: '#6B7280',    // Gray text
    white: '#FFFFFF',
    gray: '#9CA3AF',
    lightGray: '#E5E7EB',
    success: '#059669',      // Green
    warning: '#D97706',      // Amber
    danger: '#DC2626',       // Red
    info: '#0EA5E9',         // Sky blue
    gradient: {
      primary: 'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
      secondary: 'linear-gradient(135deg, #8B5CF6 0%, #6D28D9 100%)',
      accent: 'linear-gradient(135deg, #10B981 0%, #059669 100%)'
    }
  },
  fonts: {
    primary: "'Inter', sans-serif",
  },
  breakpoints: {
    mobile: '768px',
    tablet: '1024px',
    desktop: '1200px'
  }
};

export default theme;
