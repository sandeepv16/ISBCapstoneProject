# README

## Prerequisites
- **Recommended**: Minimum 12 GB of RAM and 4 vCPU for running the vision model  
- **Disk Size**: Minimum 25 GB  
- **AWS Services**: S3, EC2, Aurora Postgres instance (Optional)  

## Environment Setup (EC2)
1. Install Python and Pip using the respective Linux package managers:
   - `apt` for Ubuntu  
   - `yum` for CentOS / RHEL  

2. Install PostgreSQL database on the server. Refer to the following instructions:  
   - [PostgreSQL Installation on Linux (Official)](https://www.postgresql.org/download/linux/redhat/)  
   - [PostgreSQL Installation on Amazon Linux](https://www.linkedin.com/pulse/how-install-postgresql-amazon-linux-trong-luong-van-bfsqc/)  

3. ## Create the `steelpipes` Table

Run the following SQL command to create the `steelpipes` table:

```sql
CREATE TABLE steelpipes (
    id SERIAL PRIMARY KEY,
    image_id VARCHAR(100) NOT NULL,
    no_of_square_pipes INTEGER,
    no_of_rectangle_pipes INTEGER,
    no_of_circle_pipes INTEGER,
    no_of_hexagon_pipes INTEGER,
    total_pipes INTEGER,
    updation_time TIMESTAMPTZ
);
```

## Database Schema

Follow the below database schema for setting up the table:

| Column Name            | Data Type        | Constraints              |
|-------------------------|------------------|--------------------------|
| `id`                   | `SERIAL`         | `PRIMARY KEY`            |
| `image_id`             | `VARCHAR(100)`   | `NOT NULL`               |
| `no_of_square_pipes`   | `INTEGER`        |                          |
| `no_of_rectangle_pipes`| `INTEGER`        |                          |
| `no_of_circle_pipes`   | `INTEGER`        |                          |
| `no_of_hexagon_pipes`  | `INTEGER`        |                          |
| `total_pipes`          | `INTEGER`        |                          |
| `updation_time`        | `TIMESTAMPTZ`    |                          |


## Steps to Run the Application
1. Clone the Git repository:
   ```bash
   git clone https://github.com/ISBCapstoneProjectGroup/GENAI_Model.git -b release
2. Install the required Libraries:
    ```bash
   pip install -r requirements.txt
3. Build a config.ini file with the required information by referring to the sample file provided.
4. Run the below command to start the application:
 ```bash
    nohup streamlit run streamlit.py >> ./nohup.out &

