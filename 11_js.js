google.charts.load('current', { 'packages': ['corechart', 'bar'] });

        function handleFileSelect(event) {
            const file = event.target.files[0];
            const reader = new FileReader();

            reader.onload = function(e) {
                const csvData = e.target.result;
                parseCSV(csvData);
            };

            if (file) {
                reader.readAsText(file);
            }
        }

        function parseCSV(data) {
            const rows = data.split('\n').map(row => row.split(','));
            const headers = rows[0];
            const passengers = rows.slice(1).map(row => {
                const obj = {};
                headers.forEach((header, index) => {
                    obj[header.trim()] = row[index] ? row[index].trim() : '';
                });
                return obj;
            });

            drawCharts(passengers);
        }

        function drawCharts(data) {
            // Chart 1: Age Distribution
            const ageData = [['Age Group', 'Number of Passengers']];
            const ageGroups = { '<20': 0, '20-29': 0, '30-39': 0, '40-49': 0, '50-59': 0, '60+': 0 };

            data.forEach(row => {
                const age = parseInt(row.Age);
                if (!isNaN(age)) {
                    if (age < 20) ageGroups['<20']++;
                    else if (age < 30) ageGroups['20-29']++;
                    else if (age < 40) ageGroups['30-39']++;
                    else if (age < 50) ageGroups['40-49']++;
                    else if (age < 60) ageGroups['50-59']++;
                    else ageGroups['60+']++;
                }
            });

            for (const [ageGroup, count] of Object.entries(ageGroups)) {
                ageData.push([ageGroup, count]);
            }

            var ageOptions = {
                title: 'Passenger Age Distribution',
                hAxis: {
                    title: 'Age Group'
                },
                vAxis: {
                    title: 'Number of Passengers'
                },
                colors: ['#4CAF50']
            };

            const ageChart = new google.visualization.BarChart(document.getElementById('ageChart'));
            ageChart.draw(google.visualization.arrayToDataTable(ageData), ageOptions);

            // Chart 2: Flight Status Distribution
            const statusData = [['Flight Status', 'Number of Flights']];
            const statusCounts = { 'On Time': 0, 'Delayed': 0, 'Cancelled': 0 };

            data.forEach(row => {
                if (row['Flight Status']) {
                    statusCounts[row['Flight Status']]++;
                }
            });

            for (const [status, count] of Object.entries(statusCounts)) {
                statusData.push([status, count]);
            }

            const statusChart = new google.visualization.PieChart(document.getElementById('statusChart'));
            statusChart.draw(google.visualization.arrayToDataTable(statusData), { title: 'Flight Status Distribution' });

            // Chart 3: Gender Distribution
            const genderData = [['Gender', 'Number of Passengers']];
            const genderCounts = { Male: 0, Female: 0 };

            data.forEach(row => {
                if (row.Gender) {
                    genderCounts[row.Gender]++;
                }
            });

            for (const [gender, count] of Object.entries(genderCounts)) {
                genderData.push([gender, count]);
            }

            const genderChart = new google.visualization.PieChart(document.getElementById('genderChart'));
            genderChart.draw(google.visualization.arrayToDataTable(genderData), { title: 'Passenger Gender Distribution' });

            // Chart 4: Nationality Distribution
            const nationalityData = [['Nationality', 'Number of Passengers']];
            const nationalityCounts = {};

            data.forEach(row => {
                if (row.Nationality) {
                    nationalityCounts[row.Nationality] = (nationalityCounts[row.Nationality] || 0) + 1;
                }
            });

            for (const [nationality, count] of Object.entries(nationalityCounts)) {
                nationalityData.push([nationality, count]);
            }

            var nationalityOptions = {
                title: 'Nationality Distribution',
                hAxis: {
                    title: 'Nationality'
                },
                vAxis: {
                    title: 'Number of Passengers'
                },
                colors: ['#FFC300']
            };

            const nationalityChart = new google.visualization.BarChart(document.getElementById('nationalityChart'));
            nationalityChart.draw(google.visualization.arrayToDataTable(nationalityData), nationalityOptions);

            // Chart 5: Airport Continent Distribution
            const continentData = [['Continent', 'Number of Airports']];
            const continentCounts = {};

            data.forEach(row => {
                if (row['Airport Continent']) {
                    continentCounts[row['Airport Continent']] = (continentCounts[row['Airport Continent']] || 0) + 1;
                }
            });

            for (const [continent, count] of Object.entries(continentCounts)) {
                continentData.push([continent, count]);
            }

            var continentOptions = {
                title: 'Airport Continent Distribution',
                hAxis: {
                    title: 'Continent'
                },
                vAxis: {
                    title: 'Number of Airports'
                },
                colors: ['#673AB7']
            };
            const continentChart = new google.visualization.ColumnChart(document.getElementById('continentChart'));
            continentChart.draw(google.visualization.arrayToDataTable(continentData), continentOptions);

            // Chart 6: Flight Status by Gender
            const genderStatusData = [['Gender', 'On Time', 'Delayed', 'Cancelled']];
            const genderStatusCounts = { Male: { 'On Time': 0, 'Delayed': 0, 'Cancelled': 0 }, Female: { 'On Time': 0, 'Delayed': 0, 'Cancelled': 0 } };

            data.forEach(row => {
                const gender = row.Gender;
                const status = row['Flight Status'];
                if (genderStatusCounts[gender]) {
                    genderStatusCounts[gender][status]++;
                }
            });

            genderStatusData.push(
                ['Male', genderStatusCounts['Male']['On Time'], genderStatusCounts['Male']['Delayed'], genderStatusCounts['Male']['Cancelled']],
                ['Female', genderStatusCounts['Female']['On Time'], genderStatusCounts['Female']['Delayed'], genderStatusCounts['Female']['Cancelled']]
            );

            var genderStatusOptions = {
                title: 'Flight Status by Gender',
                hAxis: {
                    title: 'Gender'
                },
                vAxis: {
                    title: 'Number of Flights'
                },
                isStacked: true,
                colors: ['#4CAF50', '#FF5733', '#DAF7A6']
            };

            const genderStatusChart = new google.visualization.BarChart(document.getElementById('genderStatusChart'));
            genderStatusChart.draw(google.visualization.arrayToDataTable(genderStatusData), genderStatusOptions);

            // Chart 7: Average Age by Nationality
            const nationalityAgeData = [['Nationality', 'Average Age']];
            const nationalityAgeCounts = {};
            const nationalityPassengerCounts = {};

            data.forEach(row => {
                const nationality = row.Nationality;
                const age = parseInt(row.Age);
                if (!isNaN(age)) {
                    if (!nationalityAgeCounts[nationality]) {
                        nationalityAgeCounts[nationality] = 0;
                        nationalityPassengerCounts[nationality] = 0;
                    }
                    nationalityAgeCounts[nationality] += age;
                    nationalityPassengerCounts[nationality]++;
                }
            });

            for (const [nationality, totalAge] of Object.entries(nationalityAgeCounts)) {
                const avgAge = totalAge / nationalityPassengerCounts[nationality];
                nationalityAgeData.push([nationality, avgAge]);
            }

            var nationalityAgeOptions = {
                title: 'Average Age by Nationality',
                hAxis: {
                    title: 'Nationality'
                },
                vAxis: {
                    title: 'Average Age'
                },
                colors: ['#2196F3']
            };

            const nationalityAgeChart = new google.visualization.BarChart(document.getElementById('nationalityAgeChart'));
            nationalityAgeChart.draw(google.visualization.arrayToDataTable(nationalityAgeData), nationalityAgeOptions);

            // Chart 8: Number of Flights by Continent
            const flightsByContinentData = [['Continent', 'Number of Flights']];
            const flightsByContinentCounts = {};

            data.forEach(row => {
                const continent = row['Airport Continent'];
                if (continent) {
                    flightsByContinentCounts[continent] = (flightsByContinentCounts[continent] || 0) + 1;
                }
            });

            for (const [continent, count] of Object.entries(flightsByContinentCounts)) {
                flightsByContinentData.push([continent, count]);
            }

            const flightsByContinentChart = new google.visualization.BarChart(document.getElementById('flightsByContinentChart'));
            flightsByContinentChart.draw(google.visualization.arrayToDataTable(flightsByContinentData), { title: 'Number of Flights by Continent' });

            // Chart 9: Passenger Count by Arrival Airport
            const arrivalAirportData = [['Arrival Airport', 'Number of Passengers']];
            const arrivalAirportCounts = {};

            data.forEach(row => {
                const arrivalAirport = row['Arrival Airport'];
                if (arrivalAirport) {
                    arrivalAirportCounts[arrivalAirport] = (arrivalAirportCounts[arrivalAirport] || 0) + 1;
                }
            });

            for (const [airport, count] of Object.entries(arrivalAirportCounts)) {
                arrivalAirportData.push([airport, count]);
            }

            const arrivalAirportChart = new google.visualization.BarChart(document.getElementById('arrivalAirportChart'));
            arrivalAirportChart.draw(google.visualization.arrayToDataTable(arrivalAirportData), { title: 'Passenger Count by Arrival Airport' });
        }

        google.charts.setOnLoadCallback(() => {
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.csv';
            input.onchange = handleFileSelect;
            document.body.insertBefore(input, document.body.firstChild);
        });
