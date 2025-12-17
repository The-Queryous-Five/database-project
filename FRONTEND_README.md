# 🎨 Olist Analytics Dashboard - Frontend Guide

> **Modern e-commerce analytics UI built with Next.js 16, TypeScript, and Tailwind CSS**

---

## ✨ Features Overview

### 📊 Dashboard Pages

1. **Dashboard** (`/`) - Overview with stat cards and quick links
2. **Customers** (`/customers`) - Customer analytics with state search
3. **Orders** (`/orders`) - Order management with filters
4. **Products** (`/products`) - Product catalog with category filters
5. **Payments** (`/payments`) - Payment analytics by type
6. **Reviews** (`/reviews`) - Review statistics with star filters
7. **Analytics** (`/analytics`) - Advanced charts and visualizations

---

## 🎨 UI Components & Features

### Sidebar Navigation
- **Glassmorphism effect** with backdrop blur
- **Active page highlighting** with gradient background
- **Hover animations** on navigation items
- **Icons** from Lucide React
- **Responsive** - Collapsible on mobile

### Stat Cards
- **Gradient backgrounds** (purple to pink)
- **Animated counters** (future enhancement)
- **Icon integration** for visual hierarchy
- **Responsive grid** layout (1-2-4 columns)

### Data Tables
- **Gradient headers** matching theme
- **Striped rows** for readability
- **Hover effects** on rows
- **Responsive** - Horizontal scroll on mobile
- **Loading states** with spinner
- **Empty states** with helpful messages

### Search & Filters
- **Input fields** with focus states
- **Dropdown selects** with custom styling
- **Submit buttons** with hover effects
- **Real-time search** on some pages
- **Filter chips** showing active filters

---

## 🎯 Page-Specific Features

### Customers Page
**Search Controls:**
- State code input (2-letter code, e.g., "SP")
- Limit selector (10/20/50 results)

**Data Display:**
- Top cities ranking table
- Customer list with city/state info
- Total customer count

**API Integration:**
- `/customers/by-state/<state>`
- `/customers/top-cities`

---

### Orders Page
**Search Controls:**
- Order ID search
- Customer ID search
- Status filter dropdown (delivered, shipped, canceled, etc.)

**Data Display:**
- Order statistics cards
- Recent orders table with timestamps
- Order status indicators

**API Integration:**
- `/orders/stats`
- `/orders/recent`
- `/orders/by-customer/<id>`

---

### Products Page
**Search Controls:**
- Product ID search
- Category filter dropdown

**Data Display:**
- Product statistics (total products, categories)
- Product grid/table with dimensions
- Category breakdown

**API Integration:**
- `/products/stats`
- `/products?limit=N`
- `/products/by-category`
- `/products/top-categories`

---

### Payments Page
**Search Controls:**
- Payment type filter (credit_card, boleto, voucher, debit_card)

**Data Display:**
- Total payment value and count
- Average payment value
- Payment type breakdown chart
- Payment list table

**API Integration:**
- `/payments/stats`
- `/payments/by-type`

---

### Reviews Page
**Search Controls:**
- Star rating filter (1-5 stars)
- Order ID search
- Review message search

**Data Display:**
- Average review score
- Score distribution chart
- Review cards with comments
- Review timestamps

**API Integration:**
- `/reviews/stats?min_score=N&max_score=M`
- `/reviews/recent`

---

### Analytics Page
**Filters:**
- Time range selector (Today, 7/30/90 days, Year)
- Metric focus dropdown
- Chart type toggle

**Visualizations:**
- Line charts for trends
- Bar charts for comparisons
- Pie charts for distributions
- Real-time data updates

**Uses:** Recharts library for visualizations

---

## 🎨 Design System

### Color Palette
```css
Primary Gradient: from-purple-600 to-pink-500
Background: Gradient purple (667eea → 764ba2)
Text: White on dark backgrounds
Cards: Glass effect with backdrop-blur
Hover: Brightness and scale transforms
```

### Typography
- **Font**: Geist (Next.js default)
- **Headings**: Font-bold, larger sizes
- **Body**: Font-normal, readable sizes
- **Mono**: For IDs and codes

### Spacing
- **Cards**: Padding 6-8
- **Sections**: Gap 4-6
- **Forms**: Gap 4
- **Buttons**: Padding x-4, y-2

### Animations
- **Transitions**: All properties, 200-300ms
- **Hover**: Scale 105%, brightness 110%
- **Focus**: Ring with primary color
- **Loading**: Spin animation on icons

---

## 🔧 Interactive Elements

### Buttons
```tsx
// Primary button (searches, submissions)
className="bg-gradient-to-r from-purple-600 to-pink-500 text-white px-4 py-2 rounded-lg"

// Secondary button (resets, cancels)
className="bg-gray-700 text-white px-4 py-2 rounded-lg"
```

### Input Fields
```tsx
// Text input
className="bg-gray-800 border border-gray-700 text-white px-4 py-2 rounded-lg"

// Select dropdown
className="bg-gray-800 border border-gray-700 text-white px-4 py-2 rounded-lg"
```

### Loading States
```tsx
{loading && (
  <div className="flex items-center justify-center">
    <Loader2 className="animate-spin" />
    <span>Loading...</span>
  </div>
)}
```

### Error States
```tsx
{error && (
  <div className="bg-red-500/20 border border-red-500 text-red-200 p-4 rounded-lg">
    {error}
  </div>
)}
```

---

## 📱 Responsive Design

### Breakpoints (Tailwind)
- **Mobile**: Default (< 640px)
- **Tablet**: sm: (640px+)
- **Laptop**: md: (768px+)
- **Desktop**: lg: (1024px+)
- **Wide**: xl: (1280px+)

### Layout Adjustments
```tsx
// Stat cards grid
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"

// Search form
className="flex flex-col md:flex-row gap-4"

// Tables
className="overflow-x-auto" // Mobile horizontal scroll
```

---

## 🚀 Performance Features

- **Next.js App Router** for fast navigation
- **Client-side rendering** for dynamic data
- **Axios caching** (can be configured)
- **Debounced search** (future enhancement)
- **Lazy loading** for charts
- **Code splitting** by route

---

## 🎯 How to Demo

### Typical Demo Flow (5 minutes)

1. **Open Dashboard** → Show 4 stat cards with real counts
2. **Click Customers** → Search "SP" state → Show top cities
3. **Click Orders** → Filter by "delivered" status → Show order list
4. **Click Products** → Select a category → Show product details
5. **Click Payments** → Show payment breakdown chart
6. **Click Reviews** → Filter 5-star reviews → Show review cards
7. **Click Analytics** → Change time range → Show chart updates

---

## 🎨 Customization Tips

### Change Theme Colors
Edit in Tailwind classes:
```tsx
// Change primary gradient
from-purple-600 to-pink-500 → from-blue-600 to-cyan-500

// Change background
bg-gray-900 → bg-slate-900
```

### Add New Page
1. Create `olist-dashboard/app/newpage/page.tsx`
2. Add route to sidebar in `layout.tsx`
3. Create API endpoint in Flask backend
4. Use existing component patterns

### Modify Search Filters
```tsx
// Add new filter
const [newFilter, setNewFilter] = useState('')

// Add to API call
const response = await axios.get(`${API_BASE_URL}/endpoint?filter=${newFilter}`)
```

---

## 🐛 Troubleshooting

### API Not Loading
- Check Flask backend is running on port 5001
- Verify CORS is enabled in `app/app.py`
- Check browser console for errors

### Styles Not Applying
- Ensure Tailwind classes are valid
- Clear Next.js cache: `rm -rf .next`
- Restart dev server

### Components Not Updating
- Check state management in React
- Verify useEffect dependencies
- Check for console errors

---

## 📚 Tech Stack Details

### Frontend Libraries
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Icon library
- **Recharts** - Chart library
- **Axios** - HTTP client

### File Structure
```
olist-dashboard/
├── app/
│   ├── layout.tsx         # Root layout with sidebar
│   ├── page.tsx          # Dashboard home
│   ├── customers/page.tsx
│   ├── orders/page.tsx
│   ├── products/page.tsx
│   ├── payments/page.tsx
│   ├── reviews/page.tsx
│   └── analytics/page.tsx
├── public/               # Static assets
├── tailwind.config.ts    # Tailwind configuration
└── package.json          # Dependencies
```

---

<div align="center">
  <strong>For API documentation, see API_ENDPOINTS.md</strong><br>
  <strong>For setup instructions, see QUICK_START.md</strong>
</div>
open frontend/index.html
```

## 📁 Project Structure

```
database-project/
├── app/
│   ├── __init__.py
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Database configuration
│   ├── db/
│   │   └── db.py             # Database connection module
│   ├── routes/                # API endpoints
│   │   ├── customers.py
│   │   ├── orders/
│   │   ├── products.py
│   │   ├── payments.py
│   │   └── reviews.py
│   └── blueprints/            # Additional route modules
├── db/
│   ├── ddl_mysql/             # MySQL schema files
│   │   ├── 000_base.sql
│   │   ├── 010_categories.sql
│   │   ├── 020_geo_zip.sql
│   │   ├── 030_fk_v2_1.sql
│   │   └── 040_indexes.sql
│   └── etl/                   # ETL data loading scripts
│       ├── etl_utils.py
│       ├── load_categories.py
│       ├── load_customers.py
│       ├── load_sellers.py
│       ├── load_geo_zip.py
│       ├── load_products.py
│       ├── load_orders.py
│       ├── load_order_items.py
│       ├── load_payments.py
│       └── load_reviews.py
├── data/
│   └── raw/                   # CSV data files (Git LFS)
│       ├── categories.csv
│       ├── olist_customers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       └── olist_order_reviews_dataset.csv
├── frontend/
│   ├── index.html             # Main dashboard page
│   ├── css/
│   │   └── style.css         # Professional modern styling
│   └── js/
│       ├── customers.js
│       ├── orders.js
│       ├── products.js
│       ├── payments.js
│       └── reviews.js
├── scripts/
│   ├── load_all_data.sh      # Master ETL script
│   └── apply_ddl_mysql.sh    # Schema application script
├── .env                       # Environment configuration
├── requirements.txt
└── README.md
```

## 🗄️ Database Schema

### Tables (9 total)
| Table | Rows | Description |
|-------|------|-------------|
| categories | 71 | Product category translations |
| customers | 99,163 | Customer information |
| sellers | 3,088 | Seller details |
| geo_zip | 19,015 | Geolocation data by zip code |
| products | 32,951 | Product catalog |
| orders | 99,441 | Order records |
| order_items | 112,650 | Individual items per order |
| order_payments | 103,886 | Payment transactions |
| order_reviews | 98,410 | Customer reviews |

## 🎯 API Endpoints

### Customers
```
GET /customers/by-state/<state>?limit=<n>  # Get customers by state
GET /customers/top-cities?limit=<n>        # Top cities by customer count
```

### Orders
```
GET /orders/by-customer/<id>?limit=<n>     # Get customer orders
```

### Payments
```
GET /payments/by-type/<type>               # Get payments by type
```

### Reviews
```
GET /reviews/stats?min_score=<n>&max_score=<n>  # Review statistics
```

## 🎨 UI Design Features

### Color Palette
- **Primary**: Indigo (#6366f1)
- **Secondary**: Pink (#ec4899)
- **Success**: Green (#10b981)
- **Background**: Purple gradient

### Typography
- **Font**: Inter (Google Fonts)
- **Weights**: 400, 500, 600, 700, 800

### Components
- Gradient header with glassmorphism
- Hover animations on all interactive elements
- Responsive grid layouts
- Professional data tables with striped rows
- Form controls with focus states
- Loading spinners and error messages

## 🔐 Configuration

Create a `.env` file in the project root:

```env
DB_VENDOR=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=olist
DB_USER=root
DB_PASS=
```

## 🐛 Troubleshooting

### MySQL Connection Issues
```bash
# Check if MySQL is running
brew services list | grep mysql

# Restart MySQL
brew services restart mysql
```

### Data Not Loading
```bash
# Ensure autocommit is enabled in db.py
# Check that PYTHONPATH is set
export PYTHONPATH="$(pwd):$PYTHONPATH"
```

### CORS Errors
```bash
# Make sure flask-cors is installed
pip install flask-cors

# Verify CORS is enabled in app/app.py
```

## 📈 Performance

- **Page Load**: < 1s
- **API Response**: < 200ms (average)
- **Table Rendering**: Optimized for 1000+ rows
- **Database Queries**: Indexed for fast retrieval

## 🤝 Contributing

This is an academic project for Database Systems course (2025). 

## 📝 License

Educational use only - Database Systems Project 2025

## 👥 Team

Database Project Team - Fall 2025

## 🙏 Acknowledgments

- Dataset: Olist E-Commerce Public Dataset
- Framework: Flask Web Framework
- Database: MySQL Community Edition
- Fonts: Google Fonts (Inter)

---

<div align="center">
  <strong>Built with ❤️ for Database Systems Course</strong>
  <br>
  <sub>Fall 2025 Semester</sub>
</div>
