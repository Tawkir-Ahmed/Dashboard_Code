// Function to display current date and time
function updateDateTime() {
    const now = new Date();
    const dateTimeString = now.toLocaleString();
    document.getElementById('currentDateTime').textContent = `Current Date and Time: ${dateTimeString}`;
  }
  
  // Update date and time every second
  setInterval(updateDateTime, 1000);
  
  // Sample data for districts and counties (replace with real data)
  const districts = ["District 1", "District 2", "District 3"];
  const counties = {
    "District 1": ["County A", "County B"],
    "District 2": ["County C", "County D"],
    "District 3": ["County E", "County F"],
  };
  
  // Populate district dropdown
  const districtDropdown = document.getElementById('district');
  districts.forEach(district => {
    const option = document.createElement('option');
    option.value = district;
    option.textContent = district;
    districtDropdown.appendChild(option);
  });
  
  // Populate county dropdown based on selected district
  districtDropdown.addEventListener('change', () => {
    const countyDropdown = document.getElementById('county');
    countyDropdown.innerHTML = '<option value="all">All Counties</option>'; // Reset dropdown
  
    const selectedDistrict = districtDropdown.value;
    if (selectedDistrict !== "all") {
      counties[selectedDistrict].forEach(county => {
        const option = document.createElement('option');
        option.value = county;
        option.textContent = county;
        countyDropdown.appendChild(option);
      });
    }
  });
  
  // Handle search button click
  document.getElementById('searchButton').addEventListener('click', () => {
    const selectedDistrict = document.getElementById('district').value;
    const selectedCounty = document.getElementById('county').value;
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
  
    // Fetch data based on selections (replace with actual API call or data processing)
    console.log(`Searching for District: ${selectedDistrict}, County: ${selectedCounty}, Start Date: ${startDate}, End Date: ${endDate}`);
  
    // Example: Update charts and maps with new data
    updateChartsAndMaps();
  });
  

  
  // Initialize charts and maps on page load
  updateChartsAndMaps();