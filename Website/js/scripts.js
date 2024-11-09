// Toggle Sidebar Functionality
const sidebar = document.getElementById('sidebar');
const sidebarCollapseButton = document.getElementById('sidebarCollapse');
const closeSidebarButton = document.getElementById('closeSidebar');

sidebarCollapseButton.addEventListener('click', function () {
  sidebar.classList.toggle('sidebar-active');
});

closeSidebarButton.addEventListener('click', function () {
  sidebar.classList.remove('sidebar-active');
});

// js/scripts.js

var plotConfig = {
  staticPlot: false,
  editable: false,
  editSelection: false,
  showAxisRangeEntryBoxes: false,
  responsive: true,
  scrollZoom: false,
  doubleClick: false,
  showAxisDragHandles: false,
  displayModeBar: false,
  dragmode: false
};

function loadPlot(plotId, jsonFile) {
  fetch(jsonFile)
    .then((response) => response.json())
    .then((plotData) => {
      Plotly.newPlot(plotId, plotData.data, plotData.layout, plotConfig);
    })
    .catch((error) => console.error('Error loading plot:', error));
};

function tableOfContents() {
  const tocContainer = document.getElementById('table-of-contents');
  const sections = document.querySelectorAll('.section-heading');

  // Create a list element for the table of contents
  const tocList = document.createElement('ul');

  // First, add the parliamentary chart
  const sectionItem = document.createElement('li');
  const sectionLink = document.createElement('a');
  sectionLink.href = `#parliamentary-chart`;
  sectionLink.textContent = 'Parliamentary Chart';
  sectionItem.appendChild(sectionLink);
  tocList.appendChild(sectionItem);

  // Iterate through each section and add it to the list
  sections.forEach((section) => {
    // Create list item for each main section
    const sectionItem = document.createElement('li');
    const sectionLink = document.createElement('a');
    sectionLink.href = `#${section.id}`;
    sectionLink.textContent = section.textContent;
    sectionItem.appendChild(sectionLink);

    // Find all subsections within the current section
    const subsections = section.parentNode.querySelectorAll('.subsection-heading');
    if (subsections.length > 0) {
      // Create a nested list for subsections
      const subsectionList = document.createElement('ul');

      subsections.forEach((subsection) => {
        const subsectionItem = document.createElement('li');
        const subsectionLink = document.createElement('a');
        subsectionLink.href = `#${subsection.id}`;
        subsectionLink.textContent = subsection.textContent;
        subsectionItem.appendChild(subsectionLink);
        subsectionList.appendChild(subsectionItem);
      });

      sectionItem.appendChild(subsectionList);
    }

    tocList.appendChild(sectionItem);
  });

  tocContainer.appendChild(tocList);
};

function notificationStrip () {
  var notificationStrip = document.getElementById('notification-strip');
  var closeNotificationBtn = document.getElementById('close-notification');
  var navbar = document.querySelector('.navbar');

  // Check if the notification has been closed before
  if (sessionStorage.getItem('notificationClosed')) {
    notificationStrip.style.display = 'none';
    document.body.classList.remove('notification-visible');
  } else {
    // Add class to adjust navbar position
    document.body.classList.add('notification-visible');
  }

  closeNotificationBtn.addEventListener('click', function() {
    notificationStrip.style.display = 'none';
    document.body.classList.remove('notification-visible');
    sessionStorage.setItem('notificationClosed', 'true');
  });
};

// Load GeoJSON once
let globalGeoJSON = null;

function loadGeoJSON() {
  return fetch("data/output.json")
    .then((response) => response.json())
    .then((data) => {
      globalGeoJSON = data;
    })
    .catch((error) => console.error("Error loading geojson:", error));
}

// Function to recursively assign geojson data in the plot JSON
function assignGeoJSON(plotData) {
  function recursiveAssign(data) {
    if (Array.isArray(data)) {
      data.forEach(recursiveAssign);
    } else if (data && typeof data === "object") {
      for (const key in data) {
        if (key === "geojson" && data[key] === null) {
          data[key] = globalGeoJSON; // Assign global GeoJSON data
        } else if (typeof data[key] === "object") {
          recursiveAssign(data[key]);
        }
      }
    }
  }
  recursiveAssign(plotData);
}

// Modified loadPlot for map plots
function loadMapPlot(plotId, jsonFile) {
  fetch(jsonFile)
    .then((response) => response.json())
    .then((plotData) => {
      assignGeoJSON(plotData); // Inject geojson data
      Plotly.newPlot(plotId, plotData.data, plotData.layout, plotConfig);
    })
    .catch((error) => console.error("Error loading plot:", error));
}


document.addEventListener('DOMContentLoaded', function () {
  
  notificationStrip();
  tableOfContents();

  loadPlot('keh_voteshare', 'data/keh_voteshare.json');
  loadPlot('keh_constwon', 'data/keh_constwon.json');

  // Load geojson and initialize map plots after loading it
  loadGeoJSON().then(() => {
    loadMapPlot('BJYmap2018', 'data/BJYmap2018.json');
    loadMapPlot('BJYmap2023', 'data/BJYmap2023.json');
  });

  // Load other non-map plots immediately
  loadPlot('BJYvoteshare', 'data/BJYvoteshare.json');
  loadPlot('BJYconstshare', 'data/BJYconstshare.json');
  loadPlot('votesharetoptwoparties', 'data/votesharetoptwoparties.json');
  loadPlot('enop', 'data/enop.json');

});


