import { Collection } from 'backbone';
import { Category } from '../models/Category'

const Categories = Collection.extend({
    model: Category,
    url: 'http://local5/api/books',
})

export default Categories