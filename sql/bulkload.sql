/* Bulkload: 음식점 인허가 정보(영업하고 있는 업소들만) */
/* 서울마포_음식점_허가_가공.csv */
COPY "Restaurant" (manage_id, permission_date, legacy_address, address, store_name)
FROM '/path/to/서울마포_일반음식점_허가_가공.csv'
WITH (FORMAT CSV, HEADER);

/* Bulkload: 일반음식점 행정처분 정보 */
/* 서울마포_일반음식점_행정처분_가공.csv */
COPY "Action" (disposal_date, action_id, guide_date, disposal_name, legal_reason, violation, store_id)
FROM '/path/to/서울마포_일반음식점_행정처분_가공.csv'
WITH (FORMAT CSV, HEADER);