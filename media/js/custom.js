function confirm_delete(delUrl) {
  if (confirm("Are you sure you want to delete")) {
    document.location = delUrl;
  }
} 
