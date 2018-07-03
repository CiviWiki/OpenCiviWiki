import { Collection } from 'backbone';
import { Category } from '../models/Category'

const Categories = Collection.extend({
    model: Category,
    comparator: 'id'
})

export default Categories