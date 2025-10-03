from sqlalchemy.orm import Session
from typing import Any, List, Tuple, Optional
from app.base.base_error import NotFoundException
from datetime import datetime
from sqlalchemy import desc,asc, cast, Date, and_, func, or_, extract
# from app.modules.file.model import File
from app.utils.util import get_local_time

class BaseService:
    model = None  # Model harus ditentukan di kelas turunan
    module = None  # module harus ditentukan di kelas turunan
    searchable_columns: Optional[list[str]] = ["nama"]
    
    async def get_all(self, common_params, db: Session, join_relations: List[str] = None, **kwargs) -> Tuple[List, int]:
        query = db.query(self.model) # initialize query 
                
        filters = await self.filtering(common_params, join_relations)
        if filters:
            query = query.filter(*filters)

       

        # params order = name asc
        if hasattr(common_params, "order_by") and common_params.order_by is not None:
            if common_params.sort_type=="asc":
                query = query.order_by(asc(common_params.order_by))  # for descending order
            else:
                query = query.order_by(desc(common_params.order_by))  # for descending order
        elif hasattr(self.model, "created_at"):
            query = query.order_by(desc(self.model.created_at))  # for descending order    

        count = query.count() 
        page = (common_params.page - 1) * common_params.limit if common_params.page > 0 else 0
        data = query.offset(page).limit(common_params.limit).all() # apply pagination to the query
        
        return data, count

    async def filtering(self, common_params, join_relations, **kwargs):
        filters = []
        keyword_filter = f"%{common_params.keywords.lower()}%" if common_params.keywords else None

        # Handle keyword filtering for the main model
        if keyword_filter and self.searchable_columns:
            search_conditions = [
                func.lower(getattr(self.model, col)).like(keyword_filter)
                for col in self.searchable_columns if hasattr(self.model, col)
            ]
            if search_conditions:
                filters.append(or_(*search_conditions))

        # Handle keyword filtering for related models
        if keyword_filter and join_relations:
            for relation in join_relations:
                relation_class = relation.property.entity.class_
                searchable_relation_columns = getattr(relation_class, 'searchable_columns', [])
                relation_conditions = [
                    func.lower(getattr(relation_class, col)).like(keyword_filter)
                    for col in searchable_relation_columns if hasattr(relation_class, col)
                ]
                if relation_conditions:
                    filters.append(relation.has(or_(*relation_conditions)))

        # Handle attribute-based filtering
        attribute_filters = {
            "role_id": "role_id",
            "created_by": "created_by",
            "status": "status",
            "is_active": "is_active",
            "user_id": "user_id",
            "city_id": "city_id",
            "district_id": "district_id",
            "village_id": "village_id",
            "workspace_id": "workspace_id",
            "proposal_form_id":"proposal_form_id",
            "duplicate":"duplicate",
            "year": "year"
        }

        for param, attr in attribute_filters.items():
            value = getattr(common_params, param, None)
            if value is not None and hasattr(self.model, attr):
                filters.append(getattr(self.model, attr) == value)


        if hasattr(common_params, "status_ids") and common_params.status_ids is not None:
            filters.append(self.model.status_id.in_(common_params.status_ids))

        if hasattr(common_params, "ids") and common_params.ids is not None:
            filters.append(self.model.id.in_(common_params.ids))

        if hasattr(common_params, "menu_type") and common_params.menu_type is not None:
            # filters.append(self.model.menu == common_params.menu_type)
            filters.append(self.model.menu.in_(common_params.menu_type))
            # filters.append(self.model.menu == common_params.menu_type.value)

        # Handle date-based filtering
        if hasattr(common_params, "created_at") and common_params.created_at:
            filters.append(
                and_(
                    cast(self.model.start_date, Date) <= common_params.created_at.date(),
                    cast(self.model.end_date, Date) >= common_params.created_at.date()
                )
            )

        # Handle date-based filtering
        # if hasattr(common_params, "year") and common_params.year:
        #     filters.append(extract('year', self.model.created_at) == str(common_params.year))

        if hasattr(common_params, "start_date") and hasattr(common_params, "end_date"):
            start_date = common_params.start_date
            end_date = common_params.end_date.replace(hour=23, minute=59, second=59) if common_params.end_date else None
            if start_date and end_date:
                filters.append(
                    or_(
                        self.model.start_date.between(start_date, end_date),
                        self.model.time_of_incident.between(start_date, end_date),
                        self.model.departure_time.between(start_date, end_date)
                    )
                )

        return filters
        
    async def get_by_id(self, id: Any, db: Session):
        data = db.query(self.model).filter(self.model.id == id).first()
        if not data:
            raise NotFoundException(self.module, data={f"{self.module}_id":id})
        return data
    
    
    async def create(self, obj_data, db: Session):
        obj = self.model(**obj_data.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
            
 
    async def update(self, id, obj_data, db: Session):
        data = await self.get_by_id(db=db, id=id)
        if data:
            for field, value in obj_data.model_dump(exclude_unset=True).items():
                if value is not None:  # Skip fields where the value is None
                    setattr(data, field, value)
            db.commit()
            return data
        else:
            return None


    async def destroy(self, id, db: Session):
        obj = await self.get_by_id(db=db, id=id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        else:
            return False
        

    async def destroy_many(self, delete_schema, db: Session):
        db.query(self.model).filter(self.model.id.in_(delete_schema.ids)).update({"deleted_at": datetime.now()})
        db.commit()
        return True
    

    @staticmethod
    def filter_for_download(model, common_params, join_relations, **kwargs):
        filters = []
        if common_params['keywords']: # adding filter according to search parameter if there is
            if hasattr(model, "name"):
                filters.append(model.name.like(f'%{common_params["keywords"]}%'))        
            if hasattr(model, "activity"):
                filters.append(model.activity.like(f'%{common_params["keywords"]}%'))

        if 'role_id' in common_params and common_params['role_id'] is not None:
            filters.append(model.role_id == common_params['role_id'])
                              
        if 'employee_id' in common_params and common_params['employee_id'] is not None:
            filters.append(model.employee_id == common_params['employee_id'])

        if 'created_by' in common_params and common_params['created_by'] is not None:
            filters.append(model.created_by == common_params['created_by'])

        if 'current_user_id' in common_params and common_params['current_user_id'] is not None:
            filters.append(model.user_id == common_params['current_user_id'])

        if 'start_date' in common_params and common_params['start_date'] is not None and \
            'end_date' in common_params and common_params['end_date'] is not None:
            end_date = datetime.strptime(common_params['end_date'], '%Y-%m-%dT%H:%M:%S')
            end_date = end_date.replace(hour=23, minute=59, second=59)        
            
            date_range = (common_params['start_date'], end_date)
            date_fields = ['start_date', 'time_of_incident', 'departure_time']            
            for field in date_fields:
                if hasattr(model, field):
                    filters.append(getattr(model, field).between(*date_range))
                    break

        if 'time_of_incident' in common_params and common_params['time_of_incident'] is not None:
            time_of_incident = datetime.strptime(common_params['time_of_incident'], '%Y-%m-%dT%H:%M:%S')
            filters.append(cast(model.time_of_incident, Date) == time_of_incident.date())

        if 'time_incident' in common_params and common_params['time_incident'] is not None:
            time_incident = datetime.strptime(common_params['time_incident'], '%Y-%m-%dT%H:%M:%S')
            filters.append(cast(model.start_date, Date) == time_incident.date())

        if 'updated_at' in common_params and common_params['updated_at'] is not None:
            updated_at = datetime.strptime(common_params['updated_at'], '%Y-%m-%dT%H:%M:%S')
            filters.append(cast(model.updated_at, Date) == updated_at.date())

        if 'created_at' in common_params and common_params['created_at'] is not None:
            created_at = datetime.strptime(common_params['created_at'], '%Y-%m-%dT%H:%M:%S')
            filters.append(cast(model.created_at, Date) == created_at.date())

        if 'category' in common_params and common_params['category'] is not None:
            filters.append(model.category == common_params['category'])

        return filters


    async def count_and_paginate(self, query, common_params) -> Tuple[List, int]:
        count = query.count() # count total record before pagination
        data = query.offset(common_params.offset).limit(common_params.limit).all() # apply pagination to the query
        
        return data, count
    

    async def create_update_form(
        self,
        create_schema: list, 
        db: Session, 
        current_user,
        id = None
    ):
        try:
            self._prepare_form_data(create_schema, current_user)
            model = await self.update(id, obj_data=create_schema, db=db) if id else await self.create(obj_data=create_schema, db=db)
            # if model:
            #     db.query(File).filter(File.id.in_(create_schema.file_ids)).update({File.model_id: model.id})
            #     db.commit()
            return model
        except Exception as e:
            db.rollback()
            return e
    
    def _prepare_form_data(self, schema: list, current_user):
        """Prepares and sanitizes the form data."""
        schema.status = "draf" if schema.status.value == "draf" else "waiting"
        schema.employee_id = current_user.id
        if hasattr(schema, 'pay_type') and schema.pay_type:
            schema.pay_type = schema.pay_type.value
        schema.updated_at = get_local_time()


    async def reject(self, id, db):
        model = await self.get_by_id(db=db, id=id)
        model.status = "rejected"
        model.updated_at = get_local_time()
        db.commit()
        db.refresh(model)

        return model


    async def accept_all(self, schema, db):
        record = db.query(self.model).filter(self.model.id.in_(schema.ids)).update({"status": "approved","updated_at": get_local_time()})        
        db.commit()

        return record
    

    async def reject_all(self, schema, db):
        record = db.query(self.model).filter(self.model.id.in_(schema.ids)).update({"status": "rejected","updated_at": get_local_time()})        
        db.commit()

        return record
