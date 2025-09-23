# Django General Queryset

| Method                   | Example Code                                 | Description                                                                      |
|--------------------------|----------------------------------------------|----------------------------------------------------------------------------------|
| `all`                    | `MyModel.objects.all()`                     | Returns all objects in the QuerySet                                              |
| `first`                    | `MyModel.objects.all().first()`                     | Returns first data                                         |
| `exist`                    | `MyModel.objects.all().exists()`                     | Returns if exist database                                        |
| `filter`                 | `MyModel.objects.filter(field=value)`       | Filters the QuerySet by the specified field and value                            |
| `exclude`                | `MyModel.objects.exclude(field=value)`      | Excludes objects with the specified field and value from the QuerySet            |
| `get`                    | `MyModel.objects.get(field=value)`          | Retrieves a single object matching the specified field and value                 |
| `create`                 | `MyModel.objects.create(field=value)`       | Creates a new object with the specified field and value                          |
| `update`                 | `MyModel.objects.filter(field=value).update(new_field=new_value)` | Updates the objects in the QuerySet with the new field and value  |
| `delete`                 | `MyModel.objects.filter(field=value).delete()` | Deletes the objects in the QuerySet matching the specified field and value       |
| `values`                 | `MyModel.objects.values('field')`           | Returns a QuerySet containing dictionaries with the specified field values       |
| `values_list`            | `MyModel.objects.values_list('field')`      | Returns a QuerySet containing tuples with the specified field values             |
| `order_by`               | `MyModel.objects.order_by('field')`         | Orders the QuerySet by the specified field                                       |
| `distinct`               | `MyModel.objects.distinct()`                | Returns a QuerySet with distinct results based on the specified fields           |
| `count`                  | `MyModel.objects.count()`                   | Returns the number of objects in the QuerySet                                    |
| `first`                  | `MyModel.objects.first()`                   | Retrieves the first object in the QuerySet                                       |
| `last`                   | `MyModel.objects.last()`                    | Retrieves the last object in the QuerySet                                        |
| `exists`                 | `MyModel.objects.filter(field=value).exists()` | Checks if any objects in the QuerySet match the specified field and value        |
| `annotate`               | `MyModel.objects.annotate(total=Sum('field'))` | Adds an annotation to the QuerySet, such as the sum of a field's values          |
| `aggregate`              | `MyModel.objects.aggregate(total=Sum('field'))` | Returns a dictionary with the result of aggregating the specified field values   |
| `prefetch_related`       | `MyModel.objects.prefetch_related('related_field')` | Prefetches related objects, reducing the number of database queries              |
| `select_related`         | `MyModel.objects.select_related('related_field')` | Performs a SQL join and includes related fields in the QuerySet                  |
| `defer`                  | `MyModel.objects.defer('field')`            | Defers the loading of the specified field in the QuerySet                        |
| `only`                   | `MyModel.objects.only('field')`             | Loads only the specified field(s) in the QuerySet                                |
| `reverse`                | `MyModel.objects.reverse()`                 | Reverses the order of the QuerySet                                              |
| `none`                   | `MyModel.objects.none()`                    | Returns an empty QuerySet                                                        |
| `union`                  | `queryset1.union(queryset2)`                | Returns a QuerySet that is the union of two QuerySets                            |

# Here Filter list: 
```
Document: https://docs.djangoproject.com/en/4.2/ref/models/querysets/#id4
```
| Method                   | Example Code                                 | Description                                                                      |
|--------------------------|----------------------------------------------|----------------------------------------------------------------------------------|
| `pk`                      | `model.objects.get(pk=api_id, user=request.user)` | ID come from fontend by refering, user is current user two query is working here |
| `ecxclude in `  | `api = info_bulk_model.objects.filter(user=request.user).exclude(status__in=["Completed", "Failed"])` | all obj of a user without 2 condition |
| `comparing and return > ` | `model.objects.filter(int_field_name__lt=F('another_int_field_name'))` | lt(less than), and ` from django.db.models import F `|
| `comparing and return < ` | `model.objects.filter(int_field_name__gt=F('another_int_field_name'))` | gt(greater than), and ` from django.db.models import F `|
| `startswith casesensitive ` | `model.objects.filter(field_name__startswith='value')` | Here `You` and `you` is different |
| `istartswith non casesensitive ` | `model.objects.filter(field_name__istartswith='value')` | Here `You` and `you` is same |
| `endswith casesensitive ` | `model.objects.filter(field_name__endswith='value')` | Here `You` and `you` is Different |
| `iendswith non casesensitive ` | `model.objects.filter(field_name__iendswith='value')` | Here `You` and `you` is Same |
| `contains casesensitive ` | `model.objects.filter(field_name__contains='value')` | Here `You` and `you` is Different |
| `icontains non casesensitive ` | `model.objects.filter(field_name__icontains='value')` | Here `You` and `you` is Same |
| `id/int list in` | `model.objects.filter(id__in=[1, 2, 3])` | it can take multiple or Single int values, here id is int datatype |
| `name/str list in` | `model.objects.filter(name__in=['name1', 'name2', 'name3'])` | it can take multiple or Single str values, here name is str datatype |

## Example an efficient query
```py
qs = University.objects.all() # Ready for query
# Optimize related lookups
qs = qs.select_related('country', 'city').prefetch_related('bachelor_subjects', 'master_subjects', 'doctorate_subjects')

degreelevel = norm(degreelevel)
subjectname = norm(subjectname)
continent = norm(continent)
country = norm(country)
city = norm(city)

qs = University.objects.all()
# Optimize related lookups
qs = qs.select_related('country', 'city').prefetch_related('bachelor_subjects', 'master_subjects', 'doctorate_subjects')

# Continent filter (simple char field)
if continent:
    qs = qs.filter(continent__iexact=continent)

# Country filter (by name or slug)
if country:
    qs = qs.filter(Q(country__name__iexact=country) | Q(country__slug__iexact=country))

# City filter (by name or slug)
if city:
    qs = qs.filter(Q(city__name__iexact=city) | Q(city__slug__iexact=city))

# Subject filter by degree level
if subjectname:
    dl = (degreelevel or '').lower() if degreelevel else ''
    subject_q = (
        Q(bachelor_subjects__name__iexact=subjectname) | Q(bachelor_subjects__slug__iexact=subjectname) |
        Q(master_subjects__name__iexact=subjectname) | Q(master_subjects__slug__iexact=subjectname) |
        Q(doctorate_subjects__name__iexact=subjectname) | Q(doctorate_subjects__slug__iexact=subjectname)
    )
    if dl in ('bachelor', 'bachelors', "bachelor's"):
        subject_q = Q(bachelor_subjects__name__iexact=subjectname) | Q(bachelor_subjects__slug__iexact=subjectname)
    elif dl in ('master', 'masters', "master's"):
        subject_q = Q(master_subjects__name__iexact=subjectname) | Q(master_subjects__slug__iexact=subjectname)
    elif dl in ('doctorate', 'phd', 'ph.d'):
        subject_q = Q(doctorate_subjects__name__iexact=subjectname) | Q(doctorate_subjects__slug__iexact=subjectname)
    qs = qs.filter(subject_q)

qs = qs.distinct().order_by('world_rank')[:20]
serializer = UniversityListSerializer(qs, many=True)
response_data = {
    'status': 'success',
    'filters': {
        'degreelevel': degreelevel or 'All',
        'subjectname': subjectname or 'All',
        'continent': continent or 'All',
        'country': country or 'All',
        'city': city or 'All',
    },
    'count': len(serializer.data),
    'results': serializer.data,
}
logger.info("university_list served %s results", response_data['count'])
return Response(response_data, status=status.HTTP_200_OK)
except Exception as e:
logger.exception("Error in university_list: %s", str(e))
return Response({'status': 'error', 'message': f'Internal server error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

```
