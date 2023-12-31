USE [master]
GO
/****** Object:  Database [Landscape Plant Management System]    Script Date: 2023/12/4 10:52:34 ******/
CREATE DATABASE [Landscape Plant Management System]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'Landscape Plant Management System', FILENAME = N'D:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\Landscape Plant Management System.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 10%)
 LOG ON 
( NAME = N'Landscape Plant Management System_log', FILENAME = N'D:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\Landscape Plant Management System_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [Landscape Plant Management System] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [Landscape Plant Management System].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [Landscape Plant Management System] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET ARITHABORT OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [Landscape Plant Management System] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [Landscape Plant Management System] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET  DISABLE_BROKER 
GO
ALTER DATABASE [Landscape Plant Management System] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [Landscape Plant Management System] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET RECOVERY SIMPLE 
GO
ALTER DATABASE [Landscape Plant Management System] SET  MULTI_USER 
GO
ALTER DATABASE [Landscape Plant Management System] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [Landscape Plant Management System] SET DB_CHAINING OFF 
GO
ALTER DATABASE [Landscape Plant Management System] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [Landscape Plant Management System] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [Landscape Plant Management System] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [Landscape Plant Management System] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
ALTER DATABASE [Landscape Plant Management System] SET QUERY_STORE = ON
GO
ALTER DATABASE [Landscape Plant Management System] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [Landscape Plant Management System]
GO
/****** Object:  Table [dbo].[people]    Script Date: 2023/12/4 10:52:34 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[people](
	[id] [nchar](4) NOT NULL,
	[name] [nvarchar](8) NOT NULL,
	[sex] [nvarchar](10) NOT NULL,
	[task] [nvarchar](10) NOT NULL,
	[age] [nvarchar](10) NOT NULL,
 CONSTRAINT [PK_people] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plantdata]    Script Date: 2023/12/4 10:52:34 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plantdata](
	[plantid] [nchar](4) NOT NULL,
	[name] [nvarchar](10) NOT NULL,
	[othername] [nvarchar](10) NULL,
	[feature] [nvarchar](50) NOT NULL,
	[skill] [nvarchar](50) NOT NULL,
	[classificationid] [nchar](4) NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[plantpicture]    Script Date: 2023/12/4 10:52:34 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[plantpicture](
	[pictureid] [nchar](4) NOT NULL,
	[plantid] [nchar](4) NOT NULL,
	[pictureplace] [nvarchar](50) NOT NULL,
	[picturedescribe] [nvarchar](50) NOT NULL,
	[picturepeopleid] [nchar](4) NOT NULL,
	[pictureroad] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_plantpicture] PRIMARY KEY CLUSTERED 
(
	[pictureid] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [Landscape Plant Management System] SET  READ_WRITE 
GO
