from .authentication import requires_auth, requires_scope
from .transaction_functions import (_claim_ownership, _compute_nft_id,
                                    _get_identifying_id, _get_identifying_ids,
                                    _get_nft_id, _register_student, _set_id)


@requires_auth
@requires_scope('admin')
def register_student(body):
    return _register_student(body.get('ident_id'), body.get('ident_url'))

@requires_auth
@requires_scope('student')
def claim_ownership(body):
    return _claim_ownership(body.get('nft_id'), body.get('ident_id'), body.get('ident_url'), body.get('student_address'))

@requires_auth
@requires_scope('admin')
def set_id(body):
    return _set_id(body.get('nft_id'), body.get('new_ident_id'))

@requires_auth
@requires_scope('admin', 'lecturer', 'student')
def get_nft_id(**kwargs):
    if 'student_address' in kwargs:
        return _get_nft_id(kwargs['student_address'])
    elif all (k in kwargs for k in ('ident_id','ident_url')):
        return _compute_nft_id(kwargs['ident_id'], kwargs['ident_url'])
    else:
        return {"ERROR": "Wrong parameter combination. Provide student_address or ident_id and ident_url."}, 409

@requires_auth
@requires_scope('admin', 'lecturer', 'student')
def get_identifying_id(nft_id):
    return _get_identifying_id(nft_id)

@requires_auth
@requires_scope('admin', 'lecturer')
def get_identifying_ids(body):
    return _get_identifying_ids(body.get('nft_ids'))
