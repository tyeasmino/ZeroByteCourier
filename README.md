# ZeroByte Courier

## Objective
Create a RESTful API using Django Rest Framework to manage packages in a courier service. The API should allow users to perform CRUD (Create, Read, Update, Delete) operations on packages and track their status. Implement authentication and authorization to restrict access to specific operations. Ensure that no records are permanently deleted from the database during CRUD operations; instead, implement a soft delete mechanism.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/tyeasmino/ZeroByteCourier.git
   cd ZeroByteCourier

2. Install all required libraries:
    ```bash 
    pip install -r requirements.txt

3. Comment the current database-related code in settings.py:
    ```bash 
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': os.getenv('DB_NAME'),
    #         'USER': os.getenv('DB_USER'),
    #         'PASSWORD': os.getenv('DB_PASSWORD'),
    #         'HOST': os.getenv('DB_HOST'),
    #         'PORT': os.getenv('DB_PORT'),
    #     }
    # }


4. Optionally, you can create your own database and .env file to add the database details, or you  can use the default SQLite configuration. Uncomment the default database-related code:
    ```bash 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


5. Run the project:
    ```bash 
    python manage.py runserver

The server will be available at: http://127.0.0.1:8000/


6. Email verification for account registration is enabled. To enable this functionality, add the following variables to your .env file:
    ```bash 
    EMAIL_USER=your_email_user
    EMAIL_PASSWORD=your_email_password

    If these variables are not set, you will not be able to create new accounts, but other functionalities will still work.
    


## Usage Examples
### Admin Login:
### Local URL: http://127.0.0.1:8000/admin/
	Username: admin
	Password: admin for local

### if you use live link: https://zerobyte-courier.vercel.app/admin
	username: zerobyte  
	password: zerobyte
	then only http://127.0.0.1:8000 will be replace by https://zerobyte-courier.vercel.app/

### Other user login:
	Password: abcd1234%

### Registration Link: 
	http://127.0.0.1:8000/accounts/register/

### Login Link: 
	http://127.0.0.1:8000/api-auth/login/

### Office Related Links
    Locations: http://127.0.0.1:8000/office-related/locations/
    Branches: http://127.0.0.1:8000/office-related/branches/
    Parcels: http://127.0.0.1:8000/office-related/parcels/
    Parcels Receiving: http://127.0.0.1:8000/office-related/parcels-receiving/
	Note: If you're not logged in, "parcels" and "parcels-receiving" will not display anything.
	*** One More thing, if you create account that link will show you live link related url and if you click the link account will not active and you will get error


### Tracking Parcel Status
	After creating a parcel, you can track it using the tracking number. For example:
    	http://127.0.0.1:8000/office-related/tracking/WULRFT/
    	http://127.0.0.1:8000/office-related/tracking/VJ5YSV/

	For testing, you can try the following tracking codes: WULRFT, VJ5YSV, UTGM09, OKUN4O. Just replace the tracking ID after tracking/{id}.
	Note: If you're sending a parcel, you don't need to register to track its status.

### Features
    All users are office-related staff.
    A branch is automatically created when a user registers.
    Users can update branch details.
    Users can add parcels with a bill. If home delivery is added, a default charge of 100 is applied.
    Users can view receiving parcels.
    Users can update the status of receiving parcels (e.g., arrived, received, delivered).


### Technologies Used
	Django Rest Framework 

### For Free Hosting Used
	Database: Railway
	Backend: Vercel
