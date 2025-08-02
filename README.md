# Store Backend API

This Django REST Framework project provides a backend API for an e-commerce platform, supporting vendors, customers, products, orders, ratings, and more.

## Features

- **Vendor Management**: Register, login, update, and manage vendors.
- **Customer Management**: Register, login, update, and manage customers.
- **Product Management**: CRUD operations for products, including images and categories.
- **Product Search**: Search products by name or description using a search endpoint.
- **Order Management**: Place orders, manage order items, and update order status.
- **Address Management**: Customers can manage multiple addresses.
- **Product Ratings & Reviews**: Customers can rate and review products.
- **Authentication**: Basic authentication for vendors and customers.
- **Profile Pictures**: Customers and vendors can upload profile pictures.
- **Pagination**: List endpoints support pagination.

## Main Endpoints

- `/vendors/` - List or create vendors.
- `/vendor/<id>/` - Retrieve, update, or delete a vendor.
- `/vendor/login/` - Vendor login.
- `/vendor/register/` - Vendor registration.
- `/products/` - List or create products (filter by category, vendor, or id).
- `/search/` - Search products by name or description (query param `q`).
- `/product/<id>/` - Retrieve, update, or delete a product.
- `/product/<id>/add_review/` - Add a review to a product.
- `/categories/` - List or create product categories.
- `/category/<id>/` - Retrieve, update, or delete a category.
- `/customers/` - List or create customers.
- `/customer/<id>/` - Retrieve, update, or delete a customer.
- `/customer/login/` - Customer login.
- `/customer/register/` - Customer registration.
- `/orders/` - List or create orders.
- `/order/<id>/` - List order items for an order.
- `/orderitem/` - Create an order item.
- `/order-status/<order_id>/` - Update order status (PATCH).
- `/customer-dashboard/<id>/` - Get customer dashboard stats.
- `/customer-addresses/<customer_id>/` - List all addresses for a customer.
- `/vendor-order/<vendor_id>/` - List all order items for a vendor.
- `/vendor/<vendor_id>/orderitems` - Paginated order items for a vendor.
- `/vendor/<vendor_id>/customers/` - List all unique customers for a vendor.
- `/vendor/<vendor_id>/customer/<customer_id>/orders/` - List all order items for a vendor and customer.
- `/customer/change-password/` - Change customer password.
- `/vendor/change-password/` - Change vendor password.

## How It Works

- **Authentication**: Use POST requests to `/vendor/login/` or `/customer/login/` with username and password.
- **Registration**: Use POST requests to `/vendor/register/` or `/customer/register/` with required fields.
- **Product Images**: Upload images using multipart/form-data.
- **Order Placement**: Create an order, then add order items.
- **Profile Pictures**: Customers and vendors can upload or update profile pictures.
- **Ratings**: Customers can post reviews and ratings for products.

## How to Run

1. **Clone the repository** and navigate to the backend directory.

2. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

3. **Apply migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```
   python manage.py runserver
   ```

6. **Access the API** at `http://127.0.0.1:8000/`.

## Notes

- Use Django admin at `/admin/` for direct model management.
- For file uploads (images), ensure `MEDIA_ROOT` and `MEDIA_URL` are configured in your Django settings.
- Some endpoints require multipart/form-data for file uploads.
- For production, configure proper authentication and security settings.

---

**For more details, see the code and comments in each file.**
