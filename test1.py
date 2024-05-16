SELECT date, groupname, clustername, userid, particular, debit, credit, usdrate, basecurrency 
FROM ledger WHERE (date BETWEEN 2024-01-01 AND 2024-05-02 AND (client_type = overall OR client_type = ) 
                     AND basecurrency = USD AND cluster_id IN (64) AND userid_id IN (1232)) 
ORDER BY id , userid , date , basecurrency , particular , entry_type , 
client_type , debit , credit , usdrate , cluster_id , clustername , group_id 
, userid_id , groupname , usdcost 