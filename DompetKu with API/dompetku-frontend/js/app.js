const API_URL = 'http://127.0.0.1:5000/expenses';
let chart; // Untuk menyimpan instance Chart.js

document.getElementById('expense-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const date = document.getElementById('date').value;
    const type = document.getElementById('type').value;

    try {
        const res = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, amount, date, type })
        });

        if (res.ok) {
            loadExpenses();
            e.target.reset();
        } else {
            const errorData = await res.json();
            console.error("Error dari backend:", errorData);
            alert("Gagal menambahkan data:\n" + JSON.stringify(errorData, null, 2));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Gagal menghubungi server');
    }
});

async function loadExpenses() {
    const res = await fetch(API_URL);
    const data = await res.json();
    const list = document.getElementById('expense-list');
    const balanceDisplay = document.getElementById('balance');

    list.innerHTML = '';

    let total = 0;
    let totalIncome = 0;
    let totalExpense = 0;

    data.forEach(exp => {
        const li = document.createElement('li');
    
        // Tentukan warna latar belakang berdasarkan tipe
        const bgColor = exp.type === 'income' ? 'bg-green-100' : 'bg-red-100';
        const textColor = exp.type === 'income' ? 'text-green-700' : 'text-red-700';
    
        li.className = `p-3 rounded flex justify-between items-center mb-2 ${bgColor} ${textColor}`;
        li.innerHTML = `
            <div>
                <p class="font-semibold">${exp.title}</p>
                <p>Rp ${exp.amount.toLocaleString()} - ${exp.date}</p>
            </div>
            <button onclick="deleteExpense(${exp.id})" class="text-red-500">Hapus</button>
        `;
        list.appendChild(li);
    
        // Logika saldo
        if (exp.type === 'income') {
            total += exp.amount;
            totalIncome += exp.amount;
        } else if (exp.type === 'expense') {
            total -= exp.amount;
            totalExpense += exp.amount;
        }
    });    

    // Update saldo
    balanceDisplay.textContent = `Rp ${total.toLocaleString()}`;

    // Tampilkan chart total pemasukan dan pengeluaran
    renderChart(['Pemasukan', 'Pengeluaran'], [totalIncome, totalExpense], ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)']);
}

async function deleteExpense(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    loadExpenses();
}

function renderChart(labels, data, colors) {
    const ctx = document.getElementById('expenseChart').getContext('2d');
    if (chart) chart.destroy(); // Hapus chart lama jika ada

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Total (Rp)',
                data,
                backgroundColor: colors
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => `Rp ${value}`
                    }
                }
            }
        }
    });
}

loadExpenses();
