'''
BIG FAT DISCLAIMER:

This is my very first lua endeavor. Purely amateur code. 
'''



exec_multi_query_script="""

local function split(str, pat)
   local t = {}  -- NOTE: use {n = 0} in Lua-5.0
   local fpat = "(.-)" .. pat
   local last_end = 1
   local s, e, cap = str:find(fpat, 1)
   while s do
      if s ~= 1 or cap ~= "" then
     table.insert(t,cap)
      end
      last_end = e+1
      s, e, cap = str:find(fpat, last_end)
   end
   if last_end <= #str then
      cap = str:sub(last_end)
      table.insert(t, cap)
   end
   return t
end

-------------------------------------------------------------------------------

local function unfold_postings(list_of_lists)
   local new_list_of_lists = {}
   
   local transform = {}
   for i=1, #list_of_lists do
       table.insert(transform, split(list_of_lists[i], ",") )
   end
   
   for i=1, #transform do
       local nlist = {}
       local pos = 0
       for j=1, #transform[i] do
           pos = pos + transform[i][j]
           table.insert(nlist, pos)
       end
       table.insert(new_list_of_lists, nlist) 
         
    end

   return new_list_of_lists    
end

-------------------------------------------------------------------------------

local function comp(a,b)
  return #a > #b
end

-------------------------------------------------------------------------------

local function proximity_rank(list_of_lists)

        local _len = #list_of_lists

        --add padding to shorter posting
        local max = 0
        for i=1, #list_of_lists do
            if (#list_of_lists[i] > max) then max = #list_of_lists[i] end
        end
        
        
        
        local tt = {}
        
        for i, v in ipairs(list_of_lists) do
            if (#v < max) then 
               local m = v[1]
               local t = {}
                for j=#v+1, max do 
                    table.insert(t, m)
                end
                local ii=0
                for i=#t, #v+#t do
                    ii = ii + 1
                    t[i] = v[ii]
                end
                table.insert(tt, t)
            else
                 table.insert(tt, v)
            end
        end
        
        local score = 0
        local tuple = {}
        local drop = false
       
       
        while true do
            
            local tuple = {}
            for i=1, #tt do
                local a = table.remove(tt[i], 1)
                if (a and a ~= 0 ) then table.insert(tuple, a) else drop = true end
            end
            
            local i=2
            while i <= #tuple do
              if ((tuple[i] - tuple[i - 1]) < 0) then
                    table.remove(tuple, i)
                    local a = table.remove(tt[i], 1)
                    if (a and a ~= 0  and a ~= nil ) then 
                      table.insert(tuple, i, a) 
                    elseif  a == nil then
                       drop = true
                       break            
                    else 
                        i = i + 1
                    end 
              else
                  i = i + 1
              end
            end
 
            if drop then 
                break 
            else
                score = score + 1/(tuple[#tuple] - tuple[1] - _len + 1)
            end         

        end

        if score == math.huge then return 1 else
        return tostring(score)
        end
end

-------------------------------------------------------------------------------

local function weighted_ranking(tfidf, title, posting)
    local t = 0
    t = t + 0.33*tfidf + 0.33*title + 0.33*posting
    return tostring(t)

end


-------------------------------------------------------------------------------


local cardinality = redis.call('scard', '$DOCIDS$')

local terms = {}
local weights = {}
local size = #ARGV - 1
local limit = ARGV[size + 1]
local query_key = ""

for i=1, size  do
  local j = redis.call('zcard', ARGV[i])
  query_key = query_key .. ARGV[i]
  if (j ~= nil and j ~= 0) then
      table.insert(terms, ARGV[i])
      table.insert(weights, tostring(math.log((cardinality/j))))
  end
end

-- optimize, return {} if any weight is 0
if (#weights ~= size) then return {} end


local ids = {}
local tfidf = {}

-- limit query to use these ids only
if (#KEYS > 0) then

    
    for i=1, #KEYS do
      local id = redis.call('hget', "$DOCIDMAP$", KEYS[i])
      if (id) then table.insert(ids,id) end
    end
    
    
    for i=1, #ids do
        local t = 0
        for j=1, #terms do
            t = t + redis.call('zscore', terms[j], ids[i]) * weights[j]
        end
        table.insert(tfidf,t)
    end



-- normal query
else

    -- to much code to call a single zintersore
    local args = {'zinterstore', query_key, size, unpack(terms) }
    args[#args + 1] = 'WEIGHTS'
    
    for i=1, #weights do
        table.insert(args, weights[i])
    end
    
    
    redis.call(unpack(args))
    local res = redis.call('zrevrange', query_key, 0, limit, "WITHSCORES")
    
    
    

    for j=1, #res, 2 do
      table.insert(ids,res[j])
    end
    

    for j=2, #res, 2 do
      table.insert(tfidf,res[j])
    end

end


--RANKING

--RANK BY TITLE

local hits = {}

for i=1, #terms do
    for j=1, #ids do
      table.insert(hits,redis.call('sismember', 'T' .. terms[i], ids[j]))
    end
end

local t_rank = {}

for i=1, #ids do
   local cnt = i
   local sum = 0
   for j=1, #terms do
       sum = sum + hits[cnt]
       cnt = cnt + #ids
   end 
   table.insert(t_rank, sum)
end

--RANK BY POSTINGS
local post = {}
for i=1, #terms do
    table.insert(post, redis.call('hmget', '&' .. terms[i], unpack(ids)))
end

--decompose list of lists
local d_lists = {}
for i=1, #post[1] do
    local t = {}
    for j=1, #post do
        table.insert(t, post[j][i])
    end
    table.insert(d_lists, t)
end

local p_rank = {}

for i=1, #d_lists do
    table.insert(p_rank, proximity_rank(unfold_postings(d_lists[i])))
end

local results = {}


for i=1, #ids do
    table.insert(results, {redis.call('hget', "$DOCIDMAP$", ids[i]), weighted_ranking(tfidf[i], t_rank[i], p_rank[i])})
end


local function compare(a,b)
  return b[2] < a[2]
end
table.sort(results, compare)

return results

"""




exec_single_query_script = """
local query = ARGV[1]
local limit = ARGV[2]
local res = redis.call('zrevrange', query, 0, limit, "WITHSCORES")

local ids = {}
local size = #res

for i=1, size, 2 do
  table.insert(ids,{redis.call('hget', "$DOCIDMAP$", res[i]), tostring(redis.call('sismember', 'T' .. query, res[i]) + res[i+1])})
end

local function compare(a,b)
  return b[2] < a[2]
end


table.sort(ids, compare)

return ids
"""