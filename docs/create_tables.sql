-- Person info

CREATE TABLE [dbo].[Person](
	[Person_id] [varchar](5) NOT NULL,
	[Name] [varchar](20) NOT NULL,
    [Surname1] [varchar](20) NOT NULL,
    [Surname2] [varchar](20) NOT NULL,
    [Birthdate] [date] NOT NULL,
    [Pseudonim] [varchar](20) NOT NULL,
	PRIMARY KEY ([Person_id]),
)

-- Gaioles
CREATE TABLE [dbo].[Gaioles](
    [Person_id] [varchar](5) NOT NULL,
    [Day] [date] NOT NULL,
    [Instance] [int] NOT NULL,
    [Weekday] [varchar](10) NOT NULL,
    [Time_period] [varchar](7) NULL,
    PRIMARY KEY ([Person_id],[Day],[Instance]),
    FOREIGN KEY ([Person_id]) REFERENCES Person([Person_id]) ON UPDATE CASCADE ON DELETE CASCADE
)