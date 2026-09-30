const Service = require('../models/Service');

/**
 * GET /api/services
 * Returns all active services.
 */
async function getServices(req, res, next) {
  try {
    const { includeInactive } = req.query;
    const filter = includeInactive === 'true' ? {} : { active: true };

    const services = await Service.find(filter).sort({ name: 1 }).lean();
    return res.status(200).json({ success: true, count: services.length, services });
  } catch (err) {
    next(err);
  }
}

/**
 * GET /api/services/:id
 */
async function getService(req, res, next) {
  try {
    const service = await Service.findById(req.params.id).lean();
    if (!service) {
      return res.status(404).json({ success: false, message: 'Service not found.' });
    }
    return res.status(200).json({ success: true, service });
  } catch (err) {
    next(err);
  }
}

/**
 * POST /api/services
 * Creates a new service.
 */
async function createService(req, res, next) {
  try {
    const { name, code, averageDuration, description } = req.body;

    if (!name || !code) {
      return res.status(400).json({ success: false, message: 'name and code are required.' });
    }

    const existing = await Service.findOne({ code: code.toUpperCase().trim() });
    if (existing) {
      return res.status(409).json({ success: false, message: `Service code "${code}" already exists.` });
    }

    const service = await Service.create({
      name,
      code: code.toUpperCase().trim(),
      averageDuration: averageDuration || 10,
      description: description || '',
      active: true,
    });

    return res.status(201).json({ success: true, message: 'Service created.', service });
  } catch (err) {
    next(err);
  }
}

/**
 * PUT /api/services/:id
 * Updates service details.
 */
async function updateService(req, res, next) {
  try {
    const allowed = ['name', 'averageDuration', 'active', 'description'];
    const updates = {};
    for (const key of allowed) {
      if (req.body[key] !== undefined) updates[key] = req.body[key];
    }

    const service = await Service.findByIdAndUpdate(
      req.params.id,
      { $set: updates },
      { new: true, runValidators: true }
    );

    if (!service) {
      return res.status(404).json({ success: false, message: 'Service not found.' });
    }

    return res.status(200).json({ success: true, message: 'Service updated.', service });
  } catch (err) {
    next(err);
  }
}

/**
 * DELETE /api/services/:id
 * Soft-deletes a service (sets active = false).
 */
async function deleteService(req, res, next) {
  try {
    const service = await Service.findByIdAndUpdate(
      req.params.id,
      { $set: { active: false } },
      { new: true }
    );

    if (!service) {
      return res.status(404).json({ success: false, message: 'Service not found.' });
    }

    return res.status(200).json({ success: true, message: `Service "${service.name}" deactivated.` });
  } catch (err) {
    next(err);
  }
}

module.exports = { getServices, getService, createService, updateService, deleteService };
