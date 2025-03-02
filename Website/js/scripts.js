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

var mapPlotConfig = {
  staticPlot: false,
  editable: false,
  editSelection: false,
  showAxisRangeEntryBoxes: false,
  responsive: true,
  scrollZoom: false,
  doubleClick: false,
  showAxisDragHandles: false,
  displayModeBar: false,
  dragmode: false,
  staticPlot: true
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
  const sections = document.querySelectorAll('.section-start');

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
    console.log(`#${section.id}`);

    const sectionText = section.querySelector('.section-heading').textContent;
    sectionLink.textContent = sectionText;
    // sectionLink.textContent = section.textContent;
    sectionItem.appendChild(sectionLink);

    // Find all subsections within the current section
    const subsections = section.querySelectorAll('.subsection-heading');
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
      Plotly.newPlot(plotId, plotData.data, plotData.layout, mapPlotConfig);
    })
    .catch((error) => console.error("Error loading plot:", error));
}

function loadTable(id, path, fontSize = '0.8rem') {
  const container = document.getElementById(id);
  if (!container) {
    console.error(`Element with id "${id}" not found.`);
    return;
  }

  // Optional: Clear container and add a class to center its contents overall if desired
  // container.className = 'd-flex flex-column justify-content-center align-items-center';

  fetch(path)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }
      return response.json();
    })
    .then(jsonData => {
      const { title, data } = jsonData;
      if (!data || typeof data !== 'object') {
        throw new Error('Invalid data format in JSON');
      }

      const columns = Object.keys(data);
      const numRows = data[columns[0]].length;

      const table = document.createElement('table');
      // Bootstrap classes and inline style for smaller font and full width
      table.className = 'table table-bordered table-striped table-sm text-center align-middle w-100';
      table.style.fontSize = fontSize; // Adjust font-size as desired
      table.style.marginBottom = '0.6rem';

      const thead = document.createElement('thead');
      thead.style.verticalAlign = 'middle';
      const headerRow = document.createElement('tr');
      columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);

      const tbody = document.createElement('tbody');
      for (let i = 0; i < numRows; i++) {
        const row = document.createElement('tr');
        columns.forEach(col => {
          const td = document.createElement('td');
          td.textContent = data[col][i];
          row.appendChild(td);
        });
        tbody.appendChild(row);
      }

      table.appendChild(thead);
      table.appendChild(tbody);

      // Create a centered title element below the table
      const titleElement = document.createElement('h5');
      titleElement.textContent = title;
      titleElement.className = 'text-center';
      titleElement.style.fontSize = '0.9rem'; // Slightly smaller than default h2
      titleElement.style.fontWeight = 'bold';
      titleElement.style.marginTop = '0';

      container.innerHTML = '';
      // Add a wrapper to ensure everything is centered inside the container
      const wrapper = document.createElement('div');
      wrapper.className = 'w-100 d-flex flex-column justify-content-center align-items-center';
      wrapper.appendChild(table);
      wrapper.appendChild(titleElement);

      container.appendChild(wrapper);
    })
    .catch(error => {
      console.error('Error fetching or building table:', error);
      container.innerHTML = '<p class="text-danger text-center">Failed to load table data.</p>';
    });
}


document.addEventListener('DOMContentLoaded', function () {

  // Toggle Sidebar
  // sidebar.classList.toggle('sidebar-active');

  
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
  loadPlot('party_counts', 'data/party_counts.json');
  loadPlot('independent_candidates', 'data/independent_candidates.json');

  // Load table data
  loadTable('battleground-constituencies-table-bailhongal', 'data/battleground_constituencies_bailhongal.json');
  loadTable('battleground-constituencies-table-haliyal', 'data/battleground_constituencies_haliyal.json');
  loadTable('battleground-constituencies-table-hosakote', 'data/battleground_constituencies_hosakote.json');
  loadTable('battleground-constituencies-table-summary', 'data/battleground_constituencies_summary.json');
  loadTable('party-turnover-swing-direction-13-to-18', 'data/party_turnover_13to18.json', '0.95rem');
  loadTable('party-turnover-swing-direction-18-to-23', 'data/party_turnover_18to23.json', '0.95rem');

});


