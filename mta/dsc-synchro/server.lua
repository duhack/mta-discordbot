--[[
AUTHOR: duhack
GITHUB: https://github.com/duhack
WWW: https://duhack.pl/ 
]]

---BAZA DANYCH

local host = ""
local db = ""
local user = ""
local password = ""
local elementdataUID = "uid"

function connect()
    DBConnection = dbConnect( "mysql", "dbname="..db..";host="..host..";charset=utf8", user, password )
    if (not DBConnection) then
        outputDebugString("Blad: Nie udalo sie polaczyc z baza danych!")
    else
        outputDebugString("Sukces: Polaczono z baza danych!")
    end
end
addEventHandler("onResourceStart",resourceRoot, connect)

-- /discord

function insertCode(plr, code)
	dbExec( DBConnection, "INSERT INTO `synchronizacja-dsc`(`uid`, `code`, `used`) VALUES (?, ?, 'nie')", getElementData(plr, elementdataUID), code)
	setElementData(plr, "discord", code)
	outputChatBox("Wygenerowany kod do synchronizacji: "..code, plr)
	outputChatBox("Aby go zrealizować użyj komendy *synchronizacja "..code, plr)
end

function checkCode(plr, code)
	local downloadCode = dbQuery(DBConnection, "SELECT `uid` FROM `synchronizacja-dsc` WHERE code='"..code.."'")
	local result, num_affected_rows = dbPoll( downloadCode, -1 )
	if(num_affected_rows > 0) then
		outputChatBox("Wygenerowano użyty kod, ponawiam.", plr)
	else
		insertCode(plr, code)
	end
end

function syncDsc(plr)
	local tryCheck = dbQuery(DBConnection, "SELECT * FROM `synchronizacja-dsc` WHERE uid='"..getElementData(plr, elementdataUID).."'")
	local result, num_affected_rows = dbPoll( tryCheck, -1 )
	if not(num_affected_rows > 0) then
		local randomDSC = math.random(100000,999999)
		checkCode(plr, randomDSC)
	else
		for i,row in ipairs (result) do
			if row["used"] == "nie" then
			outputChatBox("Twój kod do synchronizacji: "..row["code"], plr)
			else
			outputChatBox("Twoje konto jest połączone z discordem: ("..row["account_discord"]..")", plr)
			end
		end
	end
end
addCommandHandler("discord", syncDsc)

function dscStatus(plr)
	local tryCheck = dbQuery(DBConnection, "SELECT * FROM `synchronizacja-dsc` WHERE uid='"..getElementData(plr, elementdataUID).."'")
	local result, num_affected_rows = dbPoll( tryCheck, -1 )
	if not(num_affected_rows > 0) then
		outputChatBox("Twoje konto nie jest połączone!", plr)
	else
		for i,row in ipairs (result) do
			if row["used"] == "nie" then
			outputChatBox("Twój kod do synchronizacji: "..row["code"], plr)
			else
			outputChatBox("Twoje konto jest połączone z discordem: ("..row["account_discord"]..")", plr)
			end
		end
	end
end
addCommandHandler("discord-status", dscStatus)