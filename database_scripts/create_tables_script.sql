-- Show existing databases
SHOW DATABASES;

-- Create new databas
DROP DATABASE IF EXISTS spm3;

create database spm3;

-- Use the new database
USE spm3;

-- Create Access_Control table
CREATE TABLE Access_Control (
    Access_ID int PRIMARY KEY AUTO_INCREMENT,
    Access_Control_Name varchar(50)
);

-- Create Staff table
CREATE TABLE Staff (
    Staff_ID int PRIMARY KEY,
    Staff_FName varchar(50) NOT NULL,
    Staff_LName varchar(50) NOT NULL,
    Dept varchar(50) NOT NULL,
    Country varchar(50) NOT NULL,
    Email varchar(100) NOT NULL,
    Role int,
    CONSTRAINT FK_Role_ID FOREIGN KEY (Role) REFERENCES Access_Control(Access_ID)
);

-- Create Skill table
CREATE TABLE Skill (
	Skill_ID int PRIMARY KEY AUTO_INCREMENT,
    Skill_Name varchar(250) UNIQUE,
    Skill_Desc TEXT
);

-- Create Role table
-- take note in the .csv file the column name is Role_name
CREATE TABLE Role (
	Role_ID int PRIMARY KEY AUTO_INCREMENT, 
    Role_Name varchar(250), 
    Role_Desc TEXT
);

-- Create Listing table
CREATE TABLE Listing (
	Listing_ID int PRIMARY KEY AUTO_INCREMENT, 
    Listing_Name varchar(250), 
    Listing_Desc TEXT,
    Deadline date,
    Dept varchar(50),
    HR_ID int,
    CONSTRAINT FK_HR_ID FOREIGN KEY (HR_ID) REFERENCES Staff(Staff_ID)
);

-- Create Role_Skill mapping table
CREATE TABLE Role_Skill (
    Role_ID int,
    Skill_ID int,
    CONSTRAINT PK_RoleSkill PRIMARY KEY (Role_ID, Skill_ID),
    CONSTRAINT FK_Role FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID),
    CONSTRAINT FK_Skill FOREIGN KEY (Skill_ID) REFERENCES Skill(Skill_ID)
);

-- Create Listing_Skill mapping table
CREATE TABLE Listing_Skill (
    Listing_ID int,
    Skill_ID int,
    CONSTRAINT PK_ListingSkill PRIMARY KEY (Listing_ID, Skill_ID),
    CONSTRAINT FK_Listing FOREIGN KEY (Listing_ID) REFERENCES Listing(Listing_ID),
    CONSTRAINT FK_Listing_Skill FOREIGN KEY (Skill_ID) REFERENCES Skill(Skill_ID)
);

-- Create Staff_Skill table
CREATE TABLE Staff_Skill (
    Staff_ID int,
    Skill_ID int,
    CONSTRAINT PK_StaffSkill PRIMARY KEY (Staff_ID, Skill_ID),
    CONSTRAINT FK_Staff_ID FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID),
    CONSTRAINT FK_Skill_ID FOREIGN KEY (Skill_ID) REFERENCES Skill(Skill_ID)
);

-- create Application table
CREATE TABLE Application (
    Application_ID int AUTO_INCREMENT PRIMARY KEY,
    Staff_ID int,
    Staff_Name varchar(100),
    Listing_ID int,
    Date_Applied date,
    CONSTRAINT FK_Listing_2 FOREIGN KEY (Listing_ID) REFERENCES Listing(Listing_ID),
    CONSTRAINT FK_Staff FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);
