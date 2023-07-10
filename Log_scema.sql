CREATE TABLE [run] (
  [id] integer PRIMARY KEY,
  [dt] timestamp,
  [jd] text
)
GO

CREATE TABLE [bup] (
  [id] integer PRIMARY KEY,
  [em] nvarchar(255),
  [nm] nvarchar(255),
  [run_id] integer
)
GO

CREATE TABLE [sco] (
  [id] integer PRIMARY KEY,
  [bup_id] integer,
  [run_id] integer,
  [sco] integer,
  [de] integer
)
GO

ALTER TABLE [bup] ADD FOREIGN KEY ([run_id]) REFERENCES [run] ([id])
GO

ALTER TABLE [sco] ADD FOREIGN KEY ([bup_id]) REFERENCES [bup] ([id])
GO

ALTER TABLE [sco] ADD FOREIGN KEY ([run_id]) REFERENCES [run] ([id])
GO
